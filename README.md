# GEEKLANDR Network Scanner

A simple network scanning and monitoring tool built with Python, CustomTkinter, and Nmap.

The purpose of this project is to make it easy to see devices connected to a local network through a simple graphical interface.

## Features

* 🔍 Scan the local network for devices
* 🌐 Display IP addresses
* 🖥️ Display MAC addresses
* 🏭 Display device/manufacturer information
* 🟢 Show devices that are currently online
* 📡 Background network scanning
* 🟢 Green and pink cyber/futuristic interface
* 🖥️ Graphical user interface

## How It Works

The program uses Nmap to perform a ping scan of the local network.

Example:

```bash
nmap -sn 192.168.0.0/24
```

The scanner looks for devices responding on the network and displays the results in the graphical interface.

## Requirements

If you are running the Python source code, you need:

* Python 3
* Nmap
* CustomTkinter

Install CustomTkinter:

```bash
pip install customtkinter
```

Install Nmap:

```bash
sudo apt install nmap
```

## Running the Program

From the project directory:

```bash
python network_monitor.py
```

## Project Structure

```text
GEEKLANDR-NetworkScanner/
│
├── network_monitor.py
├── logo4.png
└── README.md
```

## Future Features

Possible future improvements:

* Device names
* Port scanning
* Device history
* Network alerts
* Export scan results
* More detailed device information
* Network traffic monitoring
* Improved GUI

## Technology

Built using:

* Python
* CustomTkinter
* Nmap
* Tkinter

## Disclaimer

This tool is intended for use on networks that you own or have permission to scan.

Do not use this software to scan networks without authorization.

## Author

**GEEKLANDR**

Network tools, Linux projects, and cybersecurity learning.
