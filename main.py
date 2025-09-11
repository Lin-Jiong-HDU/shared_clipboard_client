from client.clipboard import clipboard_instance
from client.api import create_shared_clipboard, delete_shared_clipboard, get_devices_count, health_check
from client.sync import push_clipboard_content, sync_clipboard_content
import time
import threading
import sys
from blessed import Terminal
# from dashing import HSplit, VSplit, Text, Log
from dashboard import HSplit, VSplit, Text, Log
class TerminalUI:

    def __init__(self, app):
        self.term = Terminal()
        self.running = True
        self.app = app
        self.ui = self.start()
        self.log = self.ui.items[1].items[1]
        self.status_text = self.ui.items[0].items[0]
        self.clipboard_text = self.ui.items[0].items[1]
        self.menu_text = self.ui.items[1].items[0]
        self.term_height, self.term_width = self.term.height, self.term.width

        # Initialize UI content
        self.update_display()

    def start(self):
        ui = HSplit(
            VSplit(
                Text("Status", color=2, border_color=4),
                Log(title= 'Clipboard Content', color=2, border_color=4),
                Log(title='Menu', border_color=5, color=7)
            ),
            VSplit(
                Text("Connection Info", color=2, border_color=4),
                Log(title='Activity Log', border_color=3, color=7)
            ),
            title="Shared Clipboard Manager",
        )
        return ui

    def update_display(self):
        # Update status
        try:
            device_count = get_devices_count()
            health = health_check()
            status = "Connected" if health.get('status') == 'healthy' else "Disconnected"

            status_content = f"Device ID: {self.app.device_id}\n"
            status_content += f"Status: {status}\n"
            status_content += f"Connected Devices: {device_count}\n"
            status_content += f"Last Sync: {time.strftime('%H:%M:%S', time.localtime(self.app.last_sync_time))}\n"
            status_content += f"Sync Interval: {self.app.sync_interval}s"
            self.status_text.text = status_content
            # print(status_content)
        except Exception as e:
            self.status_text.text = f"Error: {str(e)}"


        # Update clipboard content
        content = self.app.clipboard_instance.get_clipboard_content()
        if len(content) > self.term_width // 2:
            display_content = f"{content[:self.term_width // 2]}..."
            chars_count = len(content)
        else:
            display_content = f"{content}\n\n[Length: {len(content)} chars]"
            chars_count = len(content)
        self.clipboard_text.append(display_content)
        self.clipboard_text.append(f"[Length: {chars_count} chars]")

        # Update menu
        menu_content = "Commands:\n"
        menu_content += "1. Manual Sync\n"
        menu_content += "2. Push Clipboard\n"
        menu_content += "3. View History\n"
        menu_content += "4. Clear History\n"
        menu_content += "5. Refresh Status\n"
        menu_content += "0. Exit"
        self.menu_text.text = menu_content

    def log_input(self, message: str):
        timestamp = time.strftime('%H:%M:%S')
        self.log.append(f"[{timestamp}] {message}")
        return

    def handle_input(self, val):
        if val.lower() == 'q' or val == '0':
            self.running = False
            self.log_input("Shutting down...")
        elif val == '1':
            self.manual_sync()
        elif val == '2':
            self.push_clipboard()
        elif val == '3':
            self.view_history()
        elif val == '4':
            self.clear_history()
        elif val == '5':
            self.update_display()
            self.log_input("Status refreshed")
        elif val:
            self.log_input(f"Pressed: {val}")

    def manual_sync(self):
        self.log_input("Performing manual sync...")
        result = sync_clipboard_content()
        self.app.last_sync_time = time.time()
        self.log_input(f"Sync Result: {result}")
        self.update_display()

    def push_clipboard(self):
        self.log_input("Pushing clipboard content...")
        result = push_clipboard_content()
        self.log_input(f"Push Result: {result}")
        self.update_display()

    def view_history(self):
        self.log_input("Retrieving clipboard history...")
        history = self.app.clipboard_instance.get_history()
        if history:
            self.log_input("Recent clipboard history:")
            for i, content in enumerate(history[-5:], 1):
                preview = content[:80] + "..." if len(content) > 80 else content
                self.log_input(f"  {i}. {preview}")
        else:
            self.log_input("No history available")

    def clear_history(self):
        self.log_input("Clearing clipboard history...")
        result = self.app.clipboard_instance.clear_history()
        self.log_input(f"Result: {result}")
        self.update_display()

    def run(self):
        term = self.term
        ui = self.ui
        with term.fullscreen(), term.hidden_cursor(), term.cbreak():

            while self.running:
                ui.display()

                val = term.inkey(timeout=0.1)
                if val:
                    self.handle_input(val)




class ClipboardApp:
    def __init__(self):
        self.running = False
        self.sync_thread = None
        self.monitor_thread = None
        self.device_id = clipboard_instance.device_id
        self.last_sync_time = 0
        self.sync_interval = 2  # seconds
        self.clipboard_instance = clipboard_instance
        self.ui = None

    def auto_sync_loop(self):
        while self.running:
            try:
                result = sync_clipboard_content()
                self.last_sync_time = time.time()
                if self.ui:
                    self.ui.log_input(f"[AUTO-SYNC] {result}")
                time.sleep(self.sync_interval)
            except Exception as e:
                if self.ui:
                    self.ui.log_input(f"[SYNC ERROR] {str(e)}")
                time.sleep(5)

    def monitor_clipboard_changes(self):
        last_content = self.clipboard_instance.get_clipboard_content()
        while self.running:
            try:
                current_content = self.clipboard_instance.get_clipboard_content()
                if current_content != last_content:
                    last_content = current_content
                    result = push_clipboard_content()
                    if self.ui:
                        self.ui.log_input(f"[AUTO-PUSH] {result}")
                time.sleep(1)
            except Exception as e:
                if self.ui:
                    self.ui.log_input(f"[MONITOR ERROR] {str(e)}")
                time.sleep(2)

    def start(self, ui):
        self.ui = ui
        self.running = True

        # Start sync thread
        self.sync_thread = threading.Thread(target=self.auto_sync_loop, daemon=True)
        self.sync_thread.start()

        # Start clipboard monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_clipboard_changes, daemon=True)
        self.monitor_thread.start()

        # Log startup
        if self.ui:
            self.ui.log_input("Clipboard sync and monitoring started")

    def stop(self):
        self.running = False
        if self.ui:
            self.ui.log_input("Clipboard sync and monitoring stopped")

def main():
    try:
        # Initialize connection to server
        print("Initializing Shared Clipboard Client...")

        # Create shared clipboard
        create_response = create_shared_clipboard()
        print(f"Connection established: {create_response}")

        # Initialize the application
        app = ClipboardApp()

        # Initialize terminal UI with app reference
        ui = TerminalUI(app)
        ui.log_input("Terminal UI initialized.")

        # Start the clipboard functionality
        app.start(ui)

        # Run the UI
        ui.run()


    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up
        try:
            delete_shared_clipboard()
            print("Connection closed.")

        except:
            pass

if __name__ == "__main__":
    main()
