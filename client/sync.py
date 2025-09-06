from client.clipboard import clipboard_instance
from client.api import sync, set_clipboard_content_for_all_devices
import time

def sync_clipboard_content():
    try:
        content = sync()
        if content == clipboard_instance.get_clipboard_content():
            return "Clipboard is already up to date."
        else:
            clipboard_instance.set_clipboard_content(content)
            return f"Clipboard updated: {len(content)} characters"
    except Exception as e:
        return f"Error during sync: {e}"

def push_clipboard_content():
    try:
        response = set_clipboard_content_for_all_devices()
        return f"Push successful: {response.get('message', 'Content pushed to all devices')}"
    except Exception as e:
        return f"Error during push: {e}"

def auto_sync_loop():
    last_content = clipboard_instance.get_clipboard_content()
    while True:
        try:
            # Check for local changes
            current_content = clipboard_instance.get_clipboard_content()
            if current_content != last_content:
                # Local change detected, push to server
                result = push_clipboard_content()
                last_content = current_content
                print(f"[AUTO-PUSH] {result}")
            else:
                # No local changes, sync from server
                result = sync_clipboard_content()
                if "Clipboard updated" in result:
                    last_content = clipboard_instance.get_clipboard_content()
                    print(f"[AUTO-SYNC] {result}")
            
            time.sleep(2)  # Check every 2 seconds
            
        except Exception as e:
            print(f"[AUTO-SYNC ERROR] {str(e)}")
            time.sleep(5)  # Wait longer on error

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
            
