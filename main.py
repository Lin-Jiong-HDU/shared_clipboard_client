from client.clipboard import clipboard_instance
from client.api import create_shared_clipboard, delete_shared_clipboard, get_devices_count, health_check, sync, set_clipboard_content_for_all_devices
from client.sync import push_clipboard_content, sync_clipboard_content
import pyperclip
import time
import threading
import os
import sys
from blessed import Terminal
from contextlib import contextmanager
from typing import Generator
from dashing import HSplit, VSplit, Text, Log

class TerminalUI:

    def __init__(self):
        self.term = Terminal()
        self.running = True
        self.ui = self.start()
        self.log = self.ui.items[0].items[2]


    def start(self):

        ui = HSplit(
            VSplit(
                Text("Shared Clipboard Client", color=2),
                Log(title='Menu', border_color=5, color=7),
                Log(title='Log', border_color=3, color=7)
            ),
            title="Shared Clipboard Manager",
        )

        return ui

    def log_input(self, message:str):
        self.log.append(message)
        return

    def run(self):
        with self.term.fullscreen(), self.term.hidden_cursor(), self.term.cbreak():
            while self.running:
                self.ui.display()

                val = self.term.inkey(timeout=0.1)
                if val.lower() == 'q':
                    self.running = False
                    break
                elif val:
                    self.log_input(f"Pressed: {val.lower()}")




class ClipboardApp:
    def __init__(self):
        self.running = False
        self.sync_thread = None
        self.device_id = clipboard_instance.device_id
        self.last_sync_time = 0
        self.sync_interval = 2  # seconds
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_header(self):
        print("=" * 60)
        print("        Shared Clipboard Client")
        print("=" * 60)
        print(f"Device ID: {self.device_id}")
        print(f"Sync Interval: {self.sync_interval}s")
        print("-" * 60)
        
    def display_status(self):
        try:
            device_count = get_devices_count()
            health = health_check()
            status = "Connected" if health.get('status') == 'healthy' else "Disconnected"
            
            print(f"Server Status: {status}")
            print(f"Connected Devices: {device_count}")
            print(f"Last Sync: {time.strftime('%H:%M:%S', time.localtime(self.last_sync_time))}")
            print("-" * 60)
            
        except Exception as e:
            print(f"Server Status: Error - {str(e)}")
            print("-" * 60)
            
    def display_clipboard_content(self):
        content = clipboard_instance.get_clipboard_content()
        print("Current Clipboard Content:")
        print("-" * 40)
        if len(content) > 200:
            print(f"{content[:200]}...")
        else:
            print(content)
        print("-" * 40)
        print(f"Length: {len(content)} characters")
        
    def auto_sync_loop(self):
        while self.running:
            try:
                result = sync_clipboard_content()
                self.last_sync_time = time.time()
                print(f"\n[SYNC] {result}")
                time.sleep(self.sync_interval)
            except Exception as e:
                print(f"\n[SYNC ERROR] {str(e)}")
                time.sleep(5)
                
    def monitor_clipboard_changes(self):
        last_content = clipboard_instance.get_clipboard_content()
        while self.running:
            try:
                current_content = clipboard_instance.get_clipboard_content()
                if current_content != last_content:
                    last_content = current_content
                    result = push_clipboard_content()
                    print(f"\n[PUSH] {result}")
                time.sleep(1)
            except Exception as e:
                print(f"\n[MONITOR ERROR] {str(e)}")
                time.sleep(2)
                
    def display_menu(self):
        print("\nCommands:")
        print("1. Manual Sync")
        print("2. Push Clipboard")
        print("3. View Clipboard History")
        print("4. Clear History")
        print("5. Refresh Status")
        print("6. Clear Screen")
        print("0. Exit")
        print("-" * 60)
        
    def manual_sync(self):
        print("\nPerforming manual sync...")
        result = sync_clipboard_content()
        self.last_sync_time = time.time()
        print(f"Sync Result: {result}")
        input("\nPress Enter to continue...")
        
    def push_clipboard(self):
        print("\nPushing clipboard content...")
        result = push_clipboard_content()
        print(f"Push Result: {result}")
        input("\nPress Enter to continue...")
        
    def view_history(self):
        print("\nClipboard History:")
        print("-" * 40)
        history = clipboard_instance.get_history()
        if history:
            for i, content in enumerate(history[-10:], 1):
                print(f"{i}. {content[:100]}{'...' if len(content) > 100 else ''}")
        else:
            print("No history available")
        input("\nPress Enter to continue...")
        
    def clear_history(self):
        print("\nClearing clipboard history...")
        result = clipboard_instance.clear_history()
        print(f"Result: {result}")
        input("\nPress Enter to continue...")
        
    def run(self, ui):
        self.running = True
        
        # Start sync thread
        self.sync_thread = threading.Thread(target=self.auto_sync_loop, daemon=True)
        self.sync_thread.start()
        
        # Start clipboard monitoring thread
        self.monitor_thread = threading.Thread(target=self.monitor_clipboard_changes, daemon=True)
        self.monitor_thread.start()
        
        # Main UI loop
        while self.running:
            self.clear_screen()
            self.display_header()
            self.display_status()
            self.display_clipboard_content()
            self.display_menu()
            self.running = ui.running
            try:
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '1':
                    self.manual_sync()
                elif choice == '2':
                    self.push_clipboard()
                elif choice == '3':
                    self.view_history()
                elif choice == '4':
                    self.clear_history()
                elif choice == '5':
                    continue  # Refresh happens automatically
                elif choice == '6':
                    continue  # Clear screen happens automatically
                elif choice == '0':
                    self.running = False
                    print("\nShutting down...")
                    break
                else:
                    print("\nInvalid choice. Please try again.")
                    time.sleep(2)
                    
            except KeyboardInterrupt:
                self.running = False
                print("\nShutting down...")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                time.sleep(2)

def main():
    try:
        # Initialize connection to server
        print("Initializing Shared Clipboard Client...")
        
        # Create shared clipboard
        create_response = create_shared_clipboard()
        print(f"Connection established: {create_response}")
        
        # Initialize terminal UI
        ui = TerminalUI()
        ui.log_input("Terminal UI initialized.")
        ui.run()

        # Start the application
        app = ClipboardApp()
        app.run(ui)

        
        
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
