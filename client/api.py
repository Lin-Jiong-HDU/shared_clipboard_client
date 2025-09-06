import requests
from uuid import uuid4
from datetime import datetime as datatime
from client.clipboard import clipboard_instance

API_URL = "http://localhost:8000/share"

def create_shared_clipboard():
    data = {
        "request_id": str(uuid4()),
        "devices_id": clipboard_instance.device_id,
        "timestamp": datatime.now().isoformat(),
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(f"{API_URL}/shared_clipboard", json=data, headers=headers)
    return response.json()

def delete_shared_clipboard():
    response = requests.delete(f"{API_URL}/shared_clipboard/{clipboard_instance.device_id}")
    return response.json()

def get_devices_count():

    headers = {
        'accept': 'application/json'
    }
    response = requests.get(f"{API_URL}/shared_clipboard", headers=headers)
    return response.json()['data']['device_count']

def set_clipboard_content():
    data = {
        "request_id": str(uuid4()),
        "devices_id": clipboard_instance.device_id,
        "timestamp": datatime.now().isoformat(),
        "data": {"content": clipboard_instance.get_clipboard_content()}
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(f"{API_URL}/shared_clipboard/set", json=data, headers=headers)
    return response.json()

def set_clipboard_content_for_all_devices():
    data = {
        "request_id": str(uuid4()),
        "devices_id": "",
        "timestamp": datatime.now().isoformat(),
        "data": {"content": clipboard_instance.get_clipboard_content()}
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(f"{API_URL}/shared_clipboard/set", json=data, headers=headers)
    return response.json()

def sync():
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(f"{API_URL}/shared_clipboard/sync", headers=headers)
    if response.status_code == 200:
        content = response.json()['data']['content']
        clipboard_instance.set_clipboard_content(content)
    return response.json()

def health_check():
    headers = {
        'accept': 'application/json'
    }
    response = requests.get(f"{API_URL}/health", headers=headers)
    return response.json()

