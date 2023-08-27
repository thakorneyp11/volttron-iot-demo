# Volttron IoT Demo

Sample implementation of a **Smart IoT Room** that elevates the capabilities of IoT devices within the Volttron ecosystem. Integrates with any devices using open protocols and stores historical data for later usage.

## 💡 Features

- Seamless Integration with IoT devices through single interface
- Historical Data Storage
- Open APIs for Data Retrieval
- Open APIs for Device Control
- Monitoring Dashboard


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

1. Download the repo using `git clone https://github.com/thakorneyp11/volttron-iot-demo.git` in your terminal or directly from github page in zip format.

2. To start Volttron platform:
```
source ~/volttron/env/bin/activate
volttron-ctl shutdown --platform  # if Volttron session already starts
volttron --bind-web-address http://0.0.0.0:8000 -vv -l ~/volttron/volttron.log&
```


<!-- ## ⚠️ Under Development!
This project is under active development and may still have issues. We appreciate your understanding and patience. If you encounter any problems, please first check the open issues. If your issue is not listed, kindly create a new issue detailing the error or problem you experienced. Thank you for your support! -->


## 👨🏻‍💻 Contributors
[![thakorneyp11](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/58812639?v=4&w=50&h=50&mask=circle)](https://github.com/thakorneyp11)
[![mcvoramet](https://images.weserv.nl/?url=https://avatars.githubusercontent.com/u/67162377?v=4&w=50&h=50&mask=circle)](https://github.com/mcvoramet)
