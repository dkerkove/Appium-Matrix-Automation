import os
import requests
import json


try:
    API_KEY = os.environ["API_KEY"]
    API_KEY = "eyJhbGciOiJSUzM4NCIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiNTIxMTQxMWEtNmU3NS00MTBmLThjOGEtODUyMjdlZGIwNjY3IiwiZG9tYWluIjoiMjUxYjQyMjQtNzE0YS00NjgzLTk0MmEtYTM1NWIyOGFlZmJmIiwibm9JT1MiOmZhbHNlLCJhZG1pbmlzdHJhdG9yIjpudWxsLCJwcm9qZWN0LWFkbWluaXN0cmF0b3IiOnRydWUsInRvdHAiOm51bGwsImVwb2NoIjpudWxsLCJmZWRlcmF0ZWRVc2VyIjpudWxsLCJpYXQiOjE3NDY4MDc5NDcsImV4cCI6MTc0NjgyOTU0N30.jh5TRluQYeORqnV3cwj3UMFeV7yvDNcHmyDH18AJZbCXHkCXp6lAIT-mlXMJ3jStEkJnw8NZNMpRriRSiXCFHAWFAMGg6dBxqJ3OQLzD4gIhTjuxXxOt05EDXYApff8n8lz5pNIh-AyHuUSrfss32i1qQT_OxWIYwgaCyCpISgDijIBq_-mmwb6uHpJg0XoB-59TqmLCwbtV0Y7b_RIxF-ESZ7SVfc3RexFT4v9XZ8iwl-9Ah-oGriLUomAZcfN7sio0zUr00MYLgQjiqDmKTvd_dqM49rj0OVT-3vdO_9TwU6FW3X5yzldd-5TnqJhavGTnre72m4I2TuROGLW-g0UhCiRZ0x46cIfsT5rwSHzsi6SS0VfEI1eILSbMSDIgLnSFVUGOguWW6zr4BVpGnuSRJEVrdlK2LA60UwmSARBSpbpfD2bgWoJ9JdRd5rVzBFtYU2odYLu7-vFJvpBbsRW6GbvDOAEjvYeLQnPDDiwQmYImcxJgBcCGfCy4vi8HCBxy5aOHl2YjSGIUij1TxfsdLLhSUtn-Q0LeUTyhIDOWbK16-miACAsBS5ijSpDluvJ0A6O5eLpcoeAasucqSaUhJv8nwSqJRvUwCxo_fhh13Paf2cTev6Ac5fnSTx5p7WWaWDoHADgk4_j2Tius49RDt9KKNOxvxSxwCEtRJIE"
except KeyError:
    API_KEY = "Token not available!"

HOST_NAME = "https://corelliumsales.enterprise.corellium.com"
INSTANCE_ID = "49ddd57d-eb27-4af7-8f43-b2dbfef35b0f"




def instance():
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    r = requests.get(f"{HOST_NAME}/api/v1/instances", headers=headers)
    if r.status_code == 200:
        data = r.json()
        device_name = data[0]['name']
        print(f'Name of first device: {device_name}')


def VMReadyCheck():
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    r = requests.get(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}/agent/v1/app/ready", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print(f"VM Ready: {data['ready']}")


def installApp(APP_NAME):
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    data = {
        "path": f"/tmp/{APP_NAME}"
    }
    r = requests.POST(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}/agent/v1/app/install", headers=headers, data=data)
    if r.status_code == 200:
        print(f"{APP_NAME} installing ...")


def startApp(BUNDLE_ID):
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    r = requests.POST(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}/agent/v1/app/apps/{BUNDLE_ID}/run", headers=headers)
    if r.status_code == 200:
        print(f"{BUNDLE_ID} started ...")


def getDevice():
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    r = requests.get(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print(data)
    

def update():
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    data = {}
    r = requests.post(f"{HOST_NAME}/api/v1/update", headers=headers, data=data)
    if r.status_code == 200:
        data = r.json()
        print(data)    


def setPortForwarding():
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    data = {"proxy":
        [
            {"devicePort":22,"routerPort":22,"expose":"false","firstAvailable":"true","status":"started"},
            {"devicePort":32,"routerPort":32,"expose":"true","firstAvailable":"true","status":"started"},
            {"devicePort":8100,"routerPort":8100,"expose":"true","firstAvailable":"false"}
        ]
    }
    r = requests.patch(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}", headers=headers, data=json.dumps(data))
    if r.status_code == 200:
        data = r.json()
        print(data)
        update()
        getDevice()
