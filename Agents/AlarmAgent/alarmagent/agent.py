"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
import time
import json

from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC

from .database_handler import insert_data

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def alarmagent(config_path, **kwargs):
    """
    Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.
    :type config_path: str
    :returns: Alarmagent
    :rtype: Alarmagent
    """
    try:
        config = utils.load_config(config_path)
    except Exception:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    device_configs = config.get("device_configs", dict())
    crate_config = config.get("crate_config", dict())
    alarm_idle_time = config.get("alarm_idle_time", 60)
    co2_threshold = config.get("co2_threshold", 1000)

    return Alarmagent(device_configs, crate_config, alarm_idle_time, co2_threshold, **kwargs)


class Alarmagent(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, device_configs=dict(), crate_config=dict(), alarm_idle_time=60, co2_threshold=1000, **kwargs):
        super(Alarmagent, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.device_configs = device_configs
        self.crate_config = crate_config
        self.alarm_idle_time = alarm_idle_time
        self.co2_threshold = co2_threshold

        self.default_config = {"device_configs": self.device_configs,
                               "crate_config": self.crate_config,
                               "alarm_idle_time": self.alarm_idle_time,
                               "co2_threshold": self.co2_threshold}

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
            crate_config = config.get("crate_config", dict())
            alarm_idle_time = config.get("alarm_idle_time", 60)
            co2_threshold = config.get("co2_threshold", 1000)
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        self.device_configs = device_configs
        self.crate_config = crate_config
        self.alarm_idle_time = alarm_idle_time
        self.co2_threshold = co2_threshold
        
        self.latest_alarm_timestamp = None
        self.device_topics = list()  # store topics of all devices

        # construct device topics and template for store latest device information
        for agent_id, device_ids in self.device_configs.items():
            _log.debug(f"{self.core.identity}: agent_id-{agent_id}, device_ids-{device_ids}")
            for device_id in device_ids:
                self.device_topics.append(f"sensor/{agent_id}/{device_id}/event")

        _log.debug(f"{self.core.identity}: self.device_topics-{self.device_topics}")

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
                                      callback=self._handle_iot_data)

    def _handle_iot_data(self, peer, sender, bus, topic, headers, message):
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

        # perform condition-based checking
        # check CO2 level more than threshold (1000ppm)
        co2_value = message.get("co2", None)
        if co2_value is None:
            return
        
        _log.debug(f"{self.core.identity}: device_id-{device_id}, co2_value-{co2_value}")

        # check alarm idle time
        if (self.latest_alarm_timestamp is None) or (time.time() - self.latest_alarm_timestamp >= self.alarm_idle_time):
            # check condition and send alarm event to CrateDB database
            if co2_value >= self.co2_threshold:
                # construct data to insert into database
                _data = [
                    time.time(),
                    device_id,
                    "alarm_co2",
                    co2_value
                ]
                # insert data into database
                insert_data(
                    table=self.crate_config.get("table_name", "raw_data"),
                    data=_data,
                    HOST=self.crate_config.get("host", "localhost"),
                    PORT=self.crate_config.get("port", 4200)
                )
                _log.debug(f"{self.core.identity}: insert Alarm data into database, data-{_data}")
                self.latest_alarm_timestamp = time.time()

        # OPTIONAL: PUBLISH alarm event to Volttron's Message Bus
        # OPTIONAL: PUBLISH control command to IoT devices
        # OPTIONAL: Send Line Notify message to LINE application


def main():
    """Main method called to start the agent."""
    utils.vip_main(alarmagent, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
