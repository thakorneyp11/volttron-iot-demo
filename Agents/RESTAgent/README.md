# REST Agent

Handle connectivity with other system outside Volttron's scope.

Example:
- open API endpoint for other system to call
- send HTTP requests to other systems
- send WebSocket protocol to other systems

To start the agent, run the following commands:
```
vctl remove --tag restagent
python ~/volttron/scripts/install-agent.py -s ~/path/to/project/Agents/RESTAgent -t restagent -i restagent
vctl config store restagent config ~/path/to/project/Agents/RESTAgent/config
vctl enable --tag restagent
vctl start --tag restagent
```
