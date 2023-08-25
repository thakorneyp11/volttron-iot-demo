"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
import json
import pendulum

from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def restagent(config_path, **kwargs):
    """
    Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.
    :type config_path: str
    :returns: RestAgent
    :rtype: RestAgent
    """
    try:
        config = utils.load_config(config_path)
    except Exception:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    device_configs = config.get("device_configs", dict())
    endpoint_device_status = config.get("endpoint_device_status", "/device/status")
    endpoint_device_control = config.get("endpoint_device_control", "/device/control")

    return RestAgent(device_configs, endpoint_device_status, endpoint_device_control, **kwargs)


class RestAgent(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, device_configs=dict(), endpoint_device_status="/device/status", endpoint_device_control="/device/control", **kwargs):
        super(RestAgent, self).__init__(enable_web=True, **kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.device_configs = device_configs
        self.endpoint_device_status = endpoint_device_status  # POST: device current status
        self.endpoint_device_control = endpoint_device_control  # POST: control device mode

        self.default_config = {"device_configs": self.device_configs,
                               "endpoint_device_status": self.endpoint_device_status,
                               "endpoint_device_control": self.endpoint_device_control}

        # Set a default configuration to ensure that self.configure is called immediately to setup
        # the agent.
        self.vip.config.set_default("config", self.default_config)
        # Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")

    def configure(self, config_name, action, contents):
        """
        Called after the Agent has connected to the message bus. If a configuration exists at startup
        this will be called before onstart.

        Is called every time the configuration in the store changes.
        """
        config = self.default_config.copy()
        config.update(contents)

        _log.debug("Configuring Agent")

        try:
            device_configs = config.get("device_configs", dict())
            endpoint_device_status = config.get("endpoint_device_status", "/device/status")
            endpoint_device_control = config.get("endpoint_device_control", "/device/control")
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return
        
        # update config values
        self.device_configs = device_configs
        self.endpoint_device_status = endpoint_device_status  # POST: device current status
        self.endpoint_device_control = endpoint_device_control  # POST: control device mode

        self.device_topics = list()  # store topics of all devices
        self.device_states = dict()  # store latest device information

        # construct device topics and template for store latest device information
        for agent_id, device_ids in self.device_configs.items():
            _log.debug(f"{self.core.identity}: agent_id-{agent_id}, device_ids-{device_ids}")
            for device_id in device_ids:
                self.device_topics.append(f"sensor/{agent_id}/{device_id}/event")
                self.device_states[str(device_id)] = dict()

        # Register REST endpoints
        self.vip.web.register_endpoint(endpoint=self.endpoint_device_status,
                                       callback=self._handle_request_device_status)
        self.vip.web.register_endpoint(endpoint=self.endpoint_device_control,
                                       callback=self._handle_request_device_control)

        _log.debug(f"{self.core.identity}: self.device_topics-{self.device_topics}")
        _log.debug(f"{self.core.identity}: self.device_states-{self.device_states}")

        self._create_subscriptions()

    def _create_subscriptions(self):
        """
        Unsubscribe from all pub/sub topics and create a subscription to a topic in the configuration which triggers
        the _handle_publish callback
        """
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        for device_topic in self.device_topics:
            self.vip.pubsub.subscribe(peer='pubsub',
                                      prefix=device_topic,
                                      callback=self._update_device_states)

    def _update_device_states(self, peer, sender, bus, topic, headers, message):
        """
        Callback triggered by the subscription setup using the topic from the agent's config file
        """
        # recheck message type
        if isinstance(message, str):
            message: dict = json.loads(message)
        
        # validate topic name
        if len(topic.split('/')) != 4:
            return
        device_id = topic.split('/')[2]
        
        # update device state (latest device information)
        self.device_states[str(device_id)] = message
        # _log.debug(f"{self.core.identity}: update latest data for `{device_id}`, device_states-{self.device_states}")

    def _handle_request_device_status(self, env, data):
        """ Return latest device information
        payload = {
            "device_id": "string",
            "datapoint_name": "string"  # (optional)
        }
        """
        _log.debug(f"{self.core.identity}: `_handle_request_device_status` Received request: {data}")

        # recheck message type
        if isinstance(data, str):
            data: dict = json.loads(data)

        # retrieve data from payload
        device_id = data.get("device_id", None)
        datapoint_name = data.get("datapoint_name", None)

        # validate payload
        if device_id is None:
            return json.dumps({"message": "device_id is required", "status_code": 400})

        # get device data from `self.device_states`
        device_data: dict() = self.device_states.get(str(device_id), dict())
        
        # construct response payload
        response_payload = device_data
        if datapoint_name is not None:
            response_payload = device_data.get(str(datapoint_name), None)

        return json.dumps({"message": response_payload, "status_code": 200})

    def _handle_request_device_control(self, env, data):
        """ Control IoT device based on payload
        payload = {
            "device_id": "string",
            "mode": "on" | "off",
        }
        """
        _log.debug(f"{self.core.identity}: `_handle_request_device_control` Received request: {data}")
        
        # recheck message type
        if isinstance(data, str):
            data: dict = json.loads(data)
        
        # retrieve data from payload
        device_id = data.get("device_id", None)
        datapoint_name = data.get("mode", None)
        
        # validate payload
        if (device_id is None) or (datapoint_name is None):
            return json.dumps({"message": "device_id and datapoint_name is required", "status_code": 400})
        
        # construct device control topic
        # obtain agent id
        device_control_topic = ""
        for agent_id, device_ids in self.device_configs.items():
            if device_id in device_ids:
                device_control_topic = f"sensor/{agent_id}/{device_id}/command"
                break
        
        if device_control_topic == "":
            return json.dumps({"message": "invalid device_id", "status_code": 400})
        
        # TODO: preprocess message
        message = data
        
        # publish message to other Agent
        self.vip.pubsub.publish(
            peer="pubsub",
            topic=device_control_topic,
            message=message,
            headers={
                "requesterID": self.core.identity,
                "message_type": "command",
                "Timestamp": pendulum.now('UTC').to_atom_string()
            }
        )
        _log.debug(f"{self.core.identity}: publish message to `{device_control_topic}`, message-{message}")

        return json.dumps({"message": data, "status_code": 200})


def main():
    """Main method called to start the agent."""
    utils.vip_main(restagent, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
