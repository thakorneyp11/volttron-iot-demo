# Alarm Agent

Perform datapoints checking and find fault cases based on designed conditions.

To start the agent, run the following commands:
```
vctl remove --tag alarm_agent
python ~/volttron/scripts/install-agent.py -s ~/path/to/project/Agents/AlarmAgent -t alarm_agent -i alarm_agent
vctl config store alarm_agent config ~/path/to/project/Agents/AlarmAgent/config
vctl enable --tag alarm_agent
vctl start --tag alarm_agent
```
