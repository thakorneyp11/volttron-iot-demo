# REST Agent

Handle connectivity with other system outside Volttron's scope.

Example:
- open API endpoint for other system to call
- send HTTP requests to other systems
- send WebSocket protocol to other systems

To start the agent, run the following commands:
```
vctl remove --tag rest_agent
python ~/volttron/scripts/install-agent.py -s ~/path/to/project/Agents/RESTAgent -t rest_agent -i rest_agent
vctl config store rest_agent config ~/path/to/project/Agents/RESTAgent/config
vctl enable --tag rest_agent
vctl start --tag rest_agent
```

There might be errors when starting the RESTAgent. Try starting Volttron platform with the following commands:
```
volttron-ctl shutdown --platform
volttron --bind-web-address http://0.0.0.0:8282 -vv -l ~/volttron/volttron.log
```
