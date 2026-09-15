# 📡 NetworkScanner

### GEEKLANDR Network Scanner

A lightweight network scanning tool with a futuristic graphical interface. NetworkScanner uses **Nmap** to discover devices on a local network and display information about them.

![NetworkScanner](logo4.png)

---

## 🚀 Download & Run

If you just want to use NetworkScanner, you **do not need Python or CustomTkinter**.

Download the `NetworkScanner` executable from this repository.

### Linux / Kali Linux

After downloading the file, open a terminal in the folder where you downloaded it and run:

```bash
chmod +x NetworkScanner
```

Then start it with:

```bash
./NetworkScanner
```

You can also move it to your Desktop:

```bash
mv NetworkScanner ~/Desktop/
```

Then run:

```bash
~/Desktop/NetworkScanner
```

---

# 🖥️ Desktop Icon

You can create a clickable desktop launcher so you don't have to use the terminal.

Create the launcher:

```bash
nano ~/Desktop/NetworkScanner.desktop
```

Paste:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Network Scanner
Comment=Network monitoring and scanning tool
Exec=/home/YOUR-USERNAME/Desktop/NetworkScanner
Icon=/home/YOUR-USERNAME/NetworkScanner/logo4.png
Terminal=false
Categories=Network;Utility;
```

Replace:

```text
YOUR-USERNAME
```

with your Linux username.

Then save the file and run:

```bash
chmod +x ~/Desktop/NetworkScanner.desktop
```

Make the launcher trusted:

```bash
gio set ~/Desktop/NetworkScanner.desktop metadata::trusted true
```

You can then launch NetworkScanner by double-clicking the desktop icon.

---

# 🔍 Features

* 📡 Local network discovery
* 🔎 Nmap-powered scanning
* 🖥️ Graphical user interface
* 🌐 IP address information
* 🔧 MAC address information
* 🏭 Device/manufacturer information
* 🟢 Futuristic green and pink interface
* 🖥️ Standalone Linux executable
* 🚫 No terminal required when launched from the desktop

---

# ⚙️ How It Works

NetworkScanner uses Nmap's ping scan:

```bash
nmap -sn 192.168.0.0/24
```

The scan looks for devices that are active on the local network.

The program then displays the discovered devices through the graphical interface.

---

# 👨‍💻 Run From Source

If you want to modify the source code, you will need Python 3 and the required packages.

## Install Nmap

On Debian/Kali-based Linux:

```bash
sudo apt install nmap
```

## Install CustomTkinter

```bash
pip install customtkinter
```

## Run NetworkScanner

From the project directory:

```bash
python network_monitor2.py
```

---

# 🛠️ Build Your Own Executable

PyInstaller can be used to create the standalone executable.

Install PyInstaller:

```bash
pip install pyinstaller
```

Then build:

```bash
python -m PyInstaller --clean --onefile --windowed --name NetworkScanner --icon=logo4.png network_monitor2.py
```

The finished executable will be created inside:

```text
dist/NetworkScanner
```

---

# 📁 Project Structure

```text
NetworkScanner/
│
├── README.md
├── network_monitor2.py
├── logo4.png
└── NetworkScanner
```

### Files

**`network_monitor2.py`**
The main Python source code.

**`logo4.png`**
The NetworkScanner application logo/icon.

**`NetworkScanner`**
The compiled standalone Linux executable.

**`README.md`**
Project documentation.

---

# 🧰 Built With

* 🐍 Python
* 🎨 CustomTkinter
* 🔎 Nmap
* 📦 PyInstaller
* 🐧 Linux

---

# 🔐 Responsible Use

NetworkScanner is intended for **authorized network administration, cybersecurity education, and testing**.

Only scan networks and devices that you own or have explicit permission to test.

Do not use NetworkScanner to scan networks without authorization.

---

# 👤 GEEKLANDR

Created as a Linux and cybersecurity learning project.

**NetworkScanner — See what's connected to your network.**
