from client.clipboard import clipboard_instance
from client.api import create_shared_clipboard, delete_shared_clipboard, get_devices_count, health_check

create_shared_clipboard()
print("Device ID:", clipboard_instance.device_id)
print("Current Clipboard Content:", clipboard_instance.get_clipboard_content())
print(get_devices_count())
response = delete_shared_clipboard()
print("Delete Response:", response)
print("Health Check:", health_check())


