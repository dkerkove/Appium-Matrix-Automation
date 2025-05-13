import os
import requests
import json
import time
import appium_cafe


try:
    API_KEY = os.environ["API_KEY"]
except KeyError:
    API_KEY = "Token not available!"

HOST_NAME = "https://corelliumsales.enterprise.corellium.com"
INSTANCE_ID = "21da5a7a-490e-4651-af4d-21a7475661a4"




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
        # resp = requests.patch(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}/agent/v1/file/device{filePath}", headers=headers, data={'mode':777})
        return filePath       


def installApp(fileName):
    headers = {
        'Authorization': f"Bearer {API_KEY}",
        'Content-Type': 'application/json'
    }
    path = uploadFile(fileName)
    # time.sleep(10)
    data = {
        "path": path
    }
    r = requests.post(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}/agent/v1/app/install", headers=headers, json=data)
    if r.status_code == 204:
        print(r)
        print(f"installing {path} ...") 


def runApp(appName):
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    r = requests.post(f"{HOST_NAME}/api/v1/instances/{INSTANCE_ID}/agent/v1/app/apps/{appName}/run", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print(f"{appName} started ...")


def createWordList():
    headers = {
        'Authorization': f"Bearer {API_KEY}",
        'Accept': 'application/json'
    }
    file = {
        'type': (None, 'mast-wordlist'),
        'encoding': (None, 'plain'),
        'instance': (None, INSTANCE_ID),
        'file': open('sensitive_values.txt', 'rb')
    }
    r = requests.post(f"{HOST_NAME}/api/v1/images", headers=headers, files=file)
    if r.status_code == 200:
        data = r.json()
        return data['id']

def createMatrixAssessment(bundle_id):
    wordlist_id = createWordList()
    headers = {
        'Authorization': f"Bearer {API_KEY}",
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'instanceId': INSTANCE_ID,
        'bundleId': bundle_id,
        'wordlistId': wordlist_id
    }
    r = requests.post(f"{HOST_NAME}/api/v1/services/matrix/{INSTANCE_ID}/assessments", headers=headers, json = data)
    if r.status_code == 200:
        data = r.json()
        return data['id']


def startMatrixMonitoring(assessment_id):
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    
    r = requests.post(f"{HOST_NAME}/api/v1/services/matrix/{INSTANCE_ID}/assessments/{assessment_id}/start", headers=headers)
    if r.status_code == 204:
        print(f"Monitoring started")
        appium_cafe.automate_app()



def stopMatrixMonitoring(assessment_id):
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    
    r = requests.post(f"{HOST_NAME}/api/v1/services/matrix/{INSTANCE_ID}/assessments/{assessment_id}/stop", headers=headers)
    if r.status_code == 204:
        print(f"Monitoring stopped")


def executeMatrixTests(assessment_id):
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    
    r = requests.post(f"{HOST_NAME}/api/v1/services/matrix/{INSTANCE_ID}/assessments/{assessment_id}/stop", headers=headers)
    if r.status_code == 200:
        data = r.json()
        print(f"Executing test")
        return data['id']


def downlodMatrixReport():
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }
    
    r = requests.post(f"{HOST_NAME}/api/v1/services/matrix/{INSTANCE_ID}/assessments/{assessment_id}/download", headers=headers)
    if r.status_code == 200:
        print(r)
