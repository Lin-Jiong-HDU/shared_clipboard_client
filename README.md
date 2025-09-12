
# Shared Clipboard Client

`shared-clipboard-client` is a command-line tool that allows you to share your clipboard content across multiple devices using a shared clipboard server. It provides a seamless way to synchronize clipboard data, monitor changes, and manage clipboard history.

![Screenshot of a terminal.](https://img.cdn1.vip/i/68c2db434f126_1757600579.webp)

## Features

- **Clipboard Synchronization**: Automatically sync clipboard content across devices.💻 📱
- **Terminal UI**: A user-friendly terminal-based interface for managing clipboard operations.
- **History Management**: View and clear clipboard history. (Not perfect)
- **Auto-Push**: Automatically push clipboard changes to the server.
- **Health Monitoring**: Check the connection status and monitor connected devices.

## Requirements

- Python 3.10 or higher
- Dependencies:
  - `blessed>=1.21.0`
  - `dashing>=0.1.0`
  - `pyperclip>=1.9.0`
  - `requests>=2.32.5`
  - `typing>=3.10.0.0`

## Installation

  _Install with `uv`_
  
1. Clone the repository:
   ```bash
   git clone https://github.com/Lin-Jiong-HDU/shared_clipboard_client
   cd shared_clipboard_client
   ```

2. Set up a virtual environment:
   ```bash
   uv venv -p 3.13.3
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

1. Start the application:
   ```bash
   python -m main.py
   ```

2. Use the terminal UI to interact with the shared clipboard:
   - **Manual Sync**: Synchronize clipboard content manually.
   - **Push Clipboard**: Push the current clipboard content to the server.
   - **View History**: Display recent clipboard history.
   - **Clear History**: Clear the clipboard history.
   - **Refresh Status**: Update the connection and device status.

3. Exit the application by pressing `0`.

> [!IMPORTANT]
> Please start the shared clipboard server first, then modify the API in `client/api.py`.\
> Link to shared clipboard server rep [SharedClipboard](https://github.com/Lin-Jiong-HDU/shared_clipboard).

## Project Structure

- `main.py`: Entry point for the application.
- `config.py`: Configuration settings for the client.
- `client/`: Contains modules for clipboard operations, API interactions, and synchronization logic.
- `dashboard/`: Implements the terminal-based UI components.
- `pyproject.toml`: Project metadata and dependencies.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
