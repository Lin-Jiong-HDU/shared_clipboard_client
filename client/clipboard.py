from uuid import uuid4
import platform
import pyperclip

class clipboard:
    def __init__(self):
        self.device_id: str = str(platform.system()) + "-" + str(uuid4())
        self.clipboard_content: str = pyperclip.paste()
        self.clipboard_content_history: list[str] = []

    def set_clipboard_content(self, content: str):
        self.clipboard_content_history.append(self.clipboard_content)
        self.clipboard_content = content
        pyperclip.copy(content)
        return "Clipboard content set."

    def get_clipboard_content(self) -> str:
        self.clipboard_content = pyperclip.paste()
        return self.clipboard_content

clipboard_instance = clipboard()
