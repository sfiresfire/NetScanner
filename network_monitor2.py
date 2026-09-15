import customtkinter as ctk
import subprocess
import threading
import re


# ============================================================
# NETWORK SETTINGS
# ============================================================

NETWORK = "192.168.0.0/24"


# ============================================================
# COLORS
# ============================================================

BLACK = "#080808"
DARK = "#101010"
DARKER = "#0B0B0B"

GREEN = "#00FF66"
GREEN_DARK = "#003B1F"

PINK = "#FF1493"
PINK_DARK = "#4A0030"

WHITE = "#FFFFFF"
GRAY = "#888888"


# ============================================================
# CUSTOMTKINTER SETTINGS
# ============================================================

ctk.set_appearance_mode("dark")


# ============================================================
# MAIN APPLICATION
# ============================================================

class NetworkMonitor(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.title("WHO HERE")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.configure(
            fg_color=BLACK
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        self.header = ctk.CTkFrame(
            self,
            fg_color=DARK,
            corner_radius=0
        )

        self.header.pack(
            fill="x"
        )

        self.title_label = ctk.CTkLabel(
            self.header,
            text="HOUSE NET",
            text_color=PINK,
            font=("Arial", 32, "bold")
        )

        self.title_label.pack(
            pady=(20, 0)
        )

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="NETWORK MONITOR",
            text_color=GREEN,
            font=("Arial", 17, "bold")
        )

        self.subtitle_label.pack(
            pady=(0, 5)
        )

        self.network_label = ctk.CTkLabel(
            self.header,
            text=f"NETWORK: {NETWORK}",
            text_color=GRAY,
            font=("Arial", 13)
        )

        self.network_label.pack(
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # CONTROL AREA
        # ----------------------------------------------------

        self.control_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.control_frame.pack(
            fill="x",
            padx=30,
            pady=20
        )

        # Scan button

        self.scan_button = ctk.CTkButton(
            self.control_frame,
            text="SCAN NETWORK",
            width=210,
            height=45,
            corner_radius=8,
            fg_color=GREEN,
            hover_color=PINK,
            text_color="black",
            font=("Arial", 15, "bold"),
            command=self.start_scan
        )

        self.scan_button.pack(
            side="left"
        )

        # Status

        self.status_label = ctk.CTkLabel(
            self.control_frame,
            text="● READY",
            text_color=GREEN,
            font=("Arial", 14, "bold")
        )

        self.status_label.pack(
            side="left",
            padx=25
        )

        # ----------------------------------------------------
        # DEVICE COUNTER
        # ----------------------------------------------------

        self.count_frame = ctk.CTkFrame(
            self,
            fg_color=DARK,
            corner_radius=8
        )

        self.count_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        self.count_label = ctk.CTkLabel(
            self.count_frame,
            text="DEVICES ONLINE: 0",
            text_color=PINK,
            font=("Arial", 18, "bold")
        )

        self.count_label.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        # ----------------------------------------------------
        # TABLE HEADER
        # ----------------------------------------------------

        self.table_header = ctk.CTkFrame(
            self,
            fg_color=GREEN_DARK,
            corner_radius=6
        )

        self.table_header.pack(
            fill="x",
            padx=30
        )

        self.create_header(
            "IP ADDRESS",
            0
        )

        self.create_header(
            "MAC ADDRESS",
            1
        )

        self.create_header(
            "MANUFACTURER",
            2
        )

        self.create_header(
            "STATUS",
            3
        )

        # ----------------------------------------------------
        # DEVICE LIST
        # ----------------------------------------------------

        self.device_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=DARKER,
            corner_radius=6
        )

        self.device_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 25)
        )

    # ========================================================
    # TABLE HEADER
    # ========================================================

    def create_header(self, text, column):

        label = ctk.CTkLabel(
            self.table_header,
            text=text,
            text_color=GREEN,
            font=("Arial", 13, "bold"),
            anchor="w"
        )

        label.grid(
            row=0,
            column=column,
            padx=20,
            pady=12,
            sticky="w"
        )

        self.table_header.grid_columnconfigure(
            column,
            weight=1
        )

    # ========================================================
    # START SCAN
    # ========================================================

    def start_scan(self):

        # Disable button while scanning

        self.scan_button.configure(
            state="disabled",
            text="SCANNING...",
            fg_color=PINK
        )

        self.status_label.configure(
            text="● SCANNING NETWORK...",
            text_color=PINK
        )

        self.count_label.configure(
            text="DEVICES ONLINE: SCANNING..."
        )

        # Remove previous devices

        for widget in self.device_frame.winfo_children():
            widget.destroy()

        # Run Nmap in background

        scan_thread = threading.Thread(
            target=self.run_nmap,
            daemon=True
        )

        scan_thread.start()

    # ========================================================
    # RUN NMAP
    # ========================================================

    def run_nmap(self):

        try:

            command = [
                "nmap",
                "-sn",
                NETWORK
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:

                self.after(
                    0,
                    lambda: self.scan_error(
                        result.stderr
                    )
                )

                return

            devices = self.parse_nmap(
                result.stdout
            )

            self.after(
                0,
                lambda: self.display_devices(
                    devices
                )
            )

        except FileNotFoundError:

            self.after(
                0,
                lambda: self.scan_error(
                    "Nmap was not found. Install it with:\n\nsudo apt install nmap"
                )
            )

        except Exception as error:

            self.after(
                0,
                lambda: self.scan_error(
                    str(error)
                )
            )

    # ========================================================
    # PARSE NMAP OUTPUT
    # ========================================================

    def parse_nmap(self, output):

        devices = []

        lines = output.splitlines()

        for line in lines:

            # -----------------------------------------------
            # FIND IP ADDRESS
            # -----------------------------------------------

            ip_match = re.search(
                r"Nmap scan report for (?:.*\()?(\d+\.\d+\.\d+\.\d+)",
                line
            )

            if ip_match:

                ip_address = ip_match.group(1)

                devices.append({
                    "ip": ip_address,
                    "mac": "Unknown",
                    "vendor": "Unknown"
                })

            # -----------------------------------------------
            # FIND MAC ADDRESS
            # -----------------------------------------------

            mac_match = re.search(
                r"MAC Address:\s+([0-9A-Fa-f:]+)\s+\((.*?)\)",
                line
            )

            if mac_match and devices:

                devices[-1]["mac"] = mac_match.group(1)

                devices[-1]["vendor"] = mac_match.group(2)

        return devices

    # ========================================================
    # DISPLAY DEVICES
    # ========================================================

    def display_devices(self, devices):

        # Update counter

        self.count_label.configure(
            text=f"DEVICES ONLINE: {len(devices)}"
        )

        # Update status

        self.status_label.configure(
            text="● SCAN COMPLETE",
            text_color=GREEN
        )

        # Restore button

        self.scan_button.configure(
            state="normal",
            text="SCAN NETWORK",
            fg_color=GREEN
        )

        # No devices

        if not devices:

            label = ctk.CTkLabel(
                self.device_frame,
                text="NO DEVICES FOUND",
                text_color=PINK,
                font=("Arial", 18, "bold")
            )

            label.pack(
                pady=40
            )

            return

        # Add every device

        for device in devices:

            self.add_device_row(
                device
            )

    # ========================================================
    # ADD DEVICE ROW
    # ========================================================

    def add_device_row(self, device):

        row = ctk.CTkFrame(
            self.device_frame,
            fg_color=DARK,
            corner_radius=6
        )

        row.pack(
            fill="x",
            pady=4
        )

        # ----------------------------------------------------
        # IP
        # ----------------------------------------------------

        ip_label = ctk.CTkLabel(
            row,
            text=device["ip"],
            text_color=WHITE,
            font=("Arial", 14),
            anchor="w"
        )

        ip_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=14,
            sticky="w"
        )

        # ----------------------------------------------------
        # MAC
        # ----------------------------------------------------

        mac_label = ctk.CTkLabel(
            row,
            text=device["mac"],
            text_color=GRAY,
            font=("Arial", 14),
            anchor="w"
        )

        mac_label.grid(
            row=0,
            column=1,
            padx=20,
            pady=14,
            sticky="w"
        )

        # ----------------------------------------------------
        # MANUFACTURER
        # ----------------------------------------------------

        vendor_label = ctk.CTkLabel(
            row,
            text=device["vendor"],
            text_color=PINK,
            font=("Arial", 14),
            anchor="w"
        )

        vendor_label.grid(
            row=0,
            column=2,
            padx=20,
            pady=14,
            sticky="w"
        )

        # ----------------------------------------------------
        # ONLINE STATUS
        # ----------------------------------------------------

        online_label = ctk.CTkLabel(
            row,
            text="● ONLINE",
            text_color=GREEN,
            font=("Arial", 14, "bold")
        )

        online_label.grid(
            row=0,
            column=3,
            padx=20,
            pady=14
        )

        # Make columns stretch

        row.grid_columnconfigure(
            0,
            weight=1
        )

        row.grid_columnconfigure(
            1,
            weight=1
        )

        row.grid_columnconfigure(
            2,
            weight=1
        )

        row.grid_columnconfigure(
            3,
            weight=1
        )

    # ========================================================
    # ERROR MESSAGE
    # ========================================================

    def scan_error(self, error):

        self.status_label.configure(
            text="● SCAN ERROR",
            text_color=PINK
        )

        self.count_label.configure(
            text="DEVICES ONLINE: 0"
        )

        self.scan_button.configure(
            state="normal",
            text="SCAN NETWORK",
            fg_color=GREEN
        )

        error_label = ctk.CTkLabel(
            self.device_frame,
            text=f"ERROR\n\n{error}",
            text_color=PINK,
            font=("Arial", 15),
            justify="center"
        )

        error_label.pack(
            pady=40
        )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    app = NetworkMonitor()

    app.mainloop()

