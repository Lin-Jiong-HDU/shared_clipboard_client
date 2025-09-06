from uuid import uuid4
import platform
import pyperclip

class clipboard:
    def __init__(self):
        self.device_id: str = str(platform.system()) + "-" + str(uuid4())
        self.clipboard_content: str = pyperclip.paste()
        self.clipboard_content_history: list[str] = []
        self.max_history_size = 50

    def set_clipboard_content(self, content: str):
        # Add current content to history before changing
        if self.clipboard_content != content:
            self.clipboard_content_history.append(self.clipboard_content)
            # Keep only the last max_history_size items
            if len(self.clipboard_content_history) > self.max_history_size:
                self.clipboard_content_history = self.clipboard_content_history[-self.max_history_size:]
        
        self.clipboard_content = content
        pyperclip.copy(content)
        return "Clipboard content set."

    def get_clipboard_content(self) -> str:
        self.clipboard_content = pyperclip.paste()
        return self.clipboard_content
    
    def get_history(self) -> list[str]:
        return self.clipboard_content_history.copy()
    
    def clear_history(self):
        self.clipboard_content_history.clear()
        return "Clipboard history cleared."

clipboard_instance = clipboard()
