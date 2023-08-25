# Volttron Agents

This folder is designed to store Volttron's Agent modules.

To create a new Agent:
| No. | Command | Description |
| -- | -- | -- |
| 1. | `source /path/to/volttron/env/bin/activate` | activate virtual environment |
| 2. | `cd /path/to/volttron/Agents` | change directory to `Agents` position |
| 3. | `vpkg init [directory name] [agent name]` | create a new Agent |

**Agent list:**
- Alarm Agent: `vpkg init AlarmAgent alarmagent`
- REST Agent: `vpkg init RESTAgenr restagent`
- TuyaIAQ Agent: `vpkg init TuyaIAQ tuya_iaq`
- TuyaSmartPlug Agent: `vpkg init TuyaSmartPlug tuya_smartplug`
