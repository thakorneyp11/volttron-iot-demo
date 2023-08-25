""" Sample code to test REST API from Volttron's RESTAgent
"""

import json
import requests


# API endpoints from Volttron's REST Agent
endpoint_device_status = "http://localhost:8282/device/status"
endpoint_device_control = "http://localhost:8282/device/control"

device_id_iaq = "eb1228790a5548d3edounv"
device_id_smartplug = "ebf90c0675a61adaa1susf"

# TEST: GET device status (all datapoint names)
response = requests.get(url=endpoint_device_status, data=json.dumps({"device_id": device_id_iaq}))
if response.status_code == 200:
    print(response.json())

# TEST: GET device status (all datapoint names)
response = requests.get(url=endpoint_device_status, data=json.dumps({"device_id": device_id_smartplug}))
if response.status_code == 200:
    print(response.json())

# TEST: GET device status (only 1 datapoint name)
response = requests.get(url=endpoint_device_status, data=json.dumps({"device_id": device_id_iaq, "datapoint_name": "va_temperature"}))
if response.status_code == 200:
    print(response.json())

# TEST: Control device mode
response = requests.post(url=endpoint_device_control, data=json.dumps({"device_id": device_id_smartplug, "mode": "off"}))
print(response.status_code)
if response.status_code == 200:
    print(response.json())
