from client.clipboard import clipboard_instance
from client.api import sync, set_clipboard_content_for_all_devices
import time

def sync_clipboard_content():
    try:
        content = sync()
        if content == clipboard_instance.get_clipboard_content():
            return "Clipboard is already up to date.\nCurrent content: " + content
        else:
            clipboard_instance.set_clipboard_content(content)
            return f"Clipboard updated to: {content}"
    except Exception as e:
        return f"Error during sync: {e}"

def push_clipboard_content():
    try:
        response = set_clipboard_content_for_all_devices()
        return f"Push Response: {response}"
    except Exception as e:
        return f"Error during push: {e}"

# def sync_push_logic():
#     last_content = clipboard_instance.get_clipboard_content()
#     while True:
#         time.sleep(2)  # Polling interval
#         current_content = clipboard_instance.get_clipboard_content()
#         if current_content != last_content:
#             last_content = current_content
#             return push_clipboard_content()
#         else:
#             return sync_clipboard_content()
            
