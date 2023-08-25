from tuya_connector import TuyaOpenAPI


def get_tuya_iaq_status(device_id: str, tuya_credential: dict()):
    # handle mapping between Tuya datapoint name and Volttron datapoint name
    TUYAENVMAP = {
        "ch2o_value": "co2",
        "va_temperature": "temperature",
        "va_humidity": "pm25",
        "pm25_value": "humidity",
        "voc_value": "noise",
        "co2_value": "illuminance"
    }
    
    # connect to Tuya OpenAPI
    openapi = TuyaOpenAPI(tuya_credential.get("api_endpoint", ""), tuya_credential.get("access_id", ""), tuya_credential.get("access_key", ""))
    openapi.connect()
    
    # get device status
    response = openapi.get(f"/v1.0/iot-03/devices/{device_id}/status", dict())
    
    # default message
    message = {
        "co2": "",
        "temperature": "",
        "pm25": "",
        "humidity": "",
        "noise": "",
        "illuminance": ""
    }
    # prepare message
    if response['success']:
        for item in response['result']:
            if item['code'] in ['ch2o_value', 'va_temperature', 'va_humidity', 'pm25_value', 'voc_value', 'co2_value']:
                message[TUYAENVMAP[item['code']]] = item['value']
    
    return message


def get_tuya_smartplug_status(device_id: str, tuya_credential: dict()):
    # connect to Tuya OpenAPI
    openapi = TuyaOpenAPI(tuya_credential.get("api_endpoint", ""), tuya_credential.get("access_id", ""), tuya_credential.get("access_key", ""))
    openapi.connect()
    
    # get device status
    response = openapi.get(f"/v1.0/iot-03/devices/{device_id}/status", dict())
    
    # default message
    message = {
        "switch_1":"",
    }
    # prepare message
    if response['success']:
        for item in response['result']:
            if item['code'] == "switch_1":
                message = {
                    item['code']: "on" if item['value'] else "off"
                }
    
    return message


def control_tuya_smartplug(device_id: str, tuya_credential: dict(), mode: str):
    __mode__ = ["on", "off"]  # mode options
    mode_dict ={
        "on": True,
        "off": False
    }

    # connect to Tuya OpenAPI
    openapi = TuyaOpenAPI(tuya_credential.get("api_endpoint", ""), tuya_credential.get("access_id", ""), tuya_credential.get("access_key", ""))
    openapi.connect()
    
    # construct command message
    command = {
        "commands": [
            {
                "code": "switch_1",
                "value": mode_dict.get(mode, False)
            }
        ]
    }
    # send command to Tuya device
    response = openapi.post(f"/v1.0/iot-03/devices/{device_id}/commands", command)
    
    return response

if __name__ == "__main__":
    # configure Tuya credential
    tuya_credential = {
        "access_id" : "mq3awcw455gy5skwkgxm",
        "access_key" : "0ecaf8cc32ae4151ad1e27ed71d5501a", 
        "api_endpoint" : "https://openapi.tuyaus.com"
    }

    # configure device id
    device_id_iaq = "eb1228790a5548d3edounv"
    device_id_smartplug = "ebf90c0675a61adaa1susf"

    # get IAQ device status
    print("Tuya IAQ sensor:")
    iaq_data = get_tuya_iaq_status(device_id_iaq, tuya_credential)
    print("iaq_data: ", iaq_data)
    
    # get SmartPlug device status
    print("Tuya SmartPlug sensor:")
    smartplug_data = get_tuya_smartplug_status(device_id_smartplug, tuya_credential)
    print("smartplug_data: ", smartplug_data)
    
    # control SmartPlug device mode
    control_tuya_smartplug(device_id_smartplug, tuya_credential, mode="off")
    
    # get SmartPlug device status
    smartplug_data = get_tuya_smartplug_status(device_id_smartplug, tuya_credential)
    print("smartplug_data: ", smartplug_data)
