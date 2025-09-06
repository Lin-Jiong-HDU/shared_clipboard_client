import requests
from uuid import uuid4
from datetime import datetime as datatime
from clipboard import clipboard_instance

API_URL = "http://localhost:8000/share"

def create_shared_clipboard():
    data = {
        "request_id": str(uuid4()),
        "device_id": clipboard_instance.device_id,
        "timestamp": datatime.now().isoformat(),
    }
    response = requests.post(f"{API_URL}/shared_clipboard", json=data)
    return response.json()

create_shared_clipboard()
