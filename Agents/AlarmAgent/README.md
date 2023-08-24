# Alarm Agent

Perform datapoints checking and find fault cases based on designed conditions.

To start the agent, run the following commands:
```
vctl remove --tag alarmagent
python ~/volttron/scripts/install-agent.py -s ~/path/to/project/Agents/AlarmAgent -t alarmagent -i alarmagent
vctl config store alarmagent config ~/path/to/project/Agents/AlarmAgent/config
vctl enable --tag alarmagent
vctl start --tag alarmagent
```

There might be errors when starting the RESTAgent. Try starting Volttron platform with the following commands:
```
volttron-ctl shutdown --platform
volttron --bind-web-address http://0.0.0.0:8282 -vv -l ~/volttron/volttron.log
```
