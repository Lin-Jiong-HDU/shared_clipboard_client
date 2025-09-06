from client.clipboard import clipboard_instance
from client.api import create_shared_clipboard, delete_shared_clipboard, get_devices_count, health_check, sync, set_clipboard_content_for_all_devices

create_shared_clipboard()
print("Device ID:", clipboard_instance.device_id)
print("Current Clipboard Content:", clipboard_instance.get_clipboard_content())
print(get_devices_count())

print(set_clipboard_content_for_all_devices())
print(sync())
response = delete_shared_clipboard()
print("Delete Response:", response)
print("Health Check:", health_check())


