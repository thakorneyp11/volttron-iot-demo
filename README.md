# Volttron IoT Demo

Sample implementation of a **Smart IoT Room** that elevates the capabilities of IoT devices within the Volttron ecosystem. Integrates with any devices using open protocols and stores historical data for later usage.

## 💡 Features

- Seamless Integration with IoT devices through single interface
- Historical Data Storage
- Open APIs for Data Retrieval
- Open APIs for Device Control
- Monitoring Dashboard
- Ease Deployment with Docker


## 💻 Images

<p align="center">
<img width=800 alt="IoT Setup" src="https://github.com/thakorneyp11/volttron-iot-demo/assets/58812639/77a64ff1-2af6-484b-a86d-53c8803afcf5" />
<img width=800 alt="Grafana Dashboard" src="https://github.com/thakorneyp11/volttron-iot-demo/assets/58812639/782c6a6d-f68a-46f0-b41f-d70ab4890378" />
</p>

## 🌐 Architecture
<details>
<summary>System Architecture</summary>

![System Architecture](https://github.com/thakorneyp11/volttron-iot-demo/assets/58812639/130d65d6-6426-4028-9365-844d75f5e058)
</details>


## ⚙️ Setting up

```bash
# clone this repository with submodules
git clone --recursive https://github.com/thakorneyp11/volttron-iot-demo.git

# or if you already cloned the repository, here's how to get the submodules
git submodule update --init --recursive

# change directory to project
cd volttron-iot-demo

# creates Volttron container with ZMQ message bus
# along with Grafana and CrateDB containers
docker-compose up -d

# to ssh into Volttron container
docker exec -itu volttron volttron1 bash

# setup an Agent: install, configure, enable, and start
vctl install /home/volttron/workspace/Agents/RESTAgent --tag rest_agent --vip-identity rest_agent
vctl config store rest_agent /home/volttron/workspace/Agents/RESTAgent/config
vctl enable --tag rest_agent
vctl start --tag rest_agent
```


<!-- ## ⚠️ Under Development!
This project is under active development and may still have issues. We appreciate your understanding and patience. If you encounter any problems, please first check the open issues. If your issue is not listed, kindly create a new issue detailing the error or problem you experienced. Thank you for your support! -->


## 👨🏻‍💻 Contributors
[![thakorneyp11](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/58812639?v=4&w=50&h=50&mask=circle)](https://github.com/thakorneyp11)
[![mcvoramet](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/67162377?v=4&w=50&h=50&mask=circle)](https://github.com/mcvoramet)
