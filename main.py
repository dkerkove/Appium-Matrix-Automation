import os
import requests
import json
import time


try:
    API_KEY = os.environ["API_KEY"]
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
            {"devicePort":22,"routerPort":22,"expose":False,"firstAvailable":True,"status":"started"},
            {"devicePort":32,"routerPort":32,"expose":True,"firstAvailable":True,"status":"started"},
            {"devicePort":8100,"routerPort":8100,"expose":True,"firstAvailable":False}
        ]
    }

    r = requests.patch(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}", headers=headers, json=data)
    if r.status_code == 200:
        data = r.json()
        print(data)


def uploadFile(fileName):
    headers = {
        'Authorization': f"Bearer {API_KEY}",
        "Content-Type": 'application/octet-stream'
    }

    filePath = f"/tmp/{fileName}"   
    
    with open(fileName, 'rb') as f:
        data = f.read()

    
    r = requests.put(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}/agent/v1/file/device{filePath}", headers=headers, data=data)
    if r.status_code == 204:
        print("uf", filePath)
        return filePath       


def installApp(fileName):
    headers = {
        'Authorization': f"Bearer {API_KEY}",
        'Content-Type': 'application/octet-stream'
    }
    path = uploadFile(fileName)
    time.sleep(3)
    print("ia", path)
    data = {
        "path": path
    }
    print(data)
    r = requests.post(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}/agent/v1/app/install", headers=headers, json=data)
    print(r.status_code)
    print(r)
    if r.status_code == 204:
        print(r) 
    
