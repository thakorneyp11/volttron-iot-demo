"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
import pendulum
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC
from volttron.platform.scheduling import periodic

from tuya_connector import (
    TuyaOpenAPI,
    TUYA_LOGGER,
)

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def tuya_iaq(config_path, **kwargs):
    """
    Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.
    :type config_path: str
    :returns: TuyaIaq
    :rtype: TuyaIaq
    """
    try:
        config = utils.load_config(config_path)
    except Exception:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    sampling_rate = config.get("sampling_rate", 5)
    tuya_credential = config.get("tuya_credential", {})
    devices = config.get("devices", [])

    return TuyaIaq(sampling_rate, tuya_credential, devices, **kwargs)



class TuyaIaq(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, sampling_rate, tuya_credential, devices, **kwargs):
        super(TuyaIaq, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.sampling_rate = sampling_rate
        self.tuya_credential = tuya_credential
        self.devices = devices

        self.default_config = {"sampling_rate": sampling_rate,
                                "tuya_credential": tuya_credential,
                                "devices": devices}

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
            sampling_rate = config.get('sampling_rate', 5)
            tuya_credential = config.get('tuya_credential', {})
            devices = config.get('devices', [])

        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        _log.info(f"IAQ CONFIG: {config}")

        self.sampling_rate = sampling_rate
        self.tuya_credential = tuya_credential
        self.devices = devices

        self.core.schedule(periodic(self.sampling_rate), self.send_sample_data)

    def send_sample_data(self):
        """
        Get data from Tuya API
        """

        # TUYAENVMAP = {"co2": "ch2o_value",
        #             "temperature": "va_temperature",
        #             "pm25": "va_humidity",
        #             "humidity": "pm25_value",
        #             "noise": "voc_value",
        #             "alarm_bright": "co2_value"
        #             }

        access_id = self.tuya_credential['access_id']
        access_key = self.tuya_credential['access_key']
        api_endpoint = self.tuya_credential['api_endpoint']
        devices = self.devices

        # Enable debug log
        TUYA_LOGGER.setLevel(logging.DEBUG)

        # Init openapi and connect
        openapi = TuyaOpenAPI(api_endpoint, access_id, access_key)
        openapi.connect()

        # Call any API from Tuya
        for device_dict in devices:
            _log.debug(f"IAQ DEVICE DICT: {device_dict.items()}")
            device_id, device_name = next(iter(device_dict.items()))
            response = openapi.get(f"/v1.0/iot-03/devices/{device_id}/status", dict())
            _log.debug(f"IAQ Agent /GET Response: {response}")
            if response['success']:
                payload = {item['code']: item['value'] for item in response['result']}
                message = {
                    "device_id": device_id,
                    "device_name": device_name,
                    "payload": payload
                }

            else:
                message = {
                    "device_id": device_id,
                    "device_name": device_name,
                    "payload": {
                        'ch2o_value': "", 
                        'alarm_bright': "", 
                        'va_temperature': "",
                        'va_humidity': "",
                        'pm25_value': "",
                        'voc_value': "",
                        'co2_value': ""
                    }
                }
        self.publish(device_id, message)

    def publish(self, device_id:str, message:dict):
        try:
            headers = {
                "requesterID": self.core.identity,
                "message_type": "event",
                "Timestamp": pendulum.now('UTC').isoformat()
            }

            topic = f"sensor/{self.core.identity}/{device_id}/event"

            self.vip.pubsub.publish(
                peer="pubsub",
                topic=topic,
                headers=headers,
                message=message
            )

            _log.info(f"{self.__class__.__name__}, Published to {topic}: {message}")

        except Exception as e:
            _log.exception(f"{self.__class__.__name__}, Error publishing to {topic}: {e}")

    def _create_subscriptions(self):
        """
        Unsubscribe from all pub/sub topics and create a subscription to a topic in the configuration which triggers
        the _handle_publish callback
        """
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=topic,
                                  callback=self._handle_publish)

    def _handle_publish(self, peer, sender, bus, topic, headers, message):
        """
        Callback triggered by the subscription setup using the topic from the agent's config file
        """
        pass

    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        # Example publish to pubsub
        self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        # Example RPC call
        # self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
        pass

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.core.rpc.call
        """
        return self.setting1 + arg1 - arg2


def main():
    """Main method called to start the agent."""
    utils.vip_main(tuya_iaq, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
