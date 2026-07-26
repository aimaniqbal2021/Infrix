import datetime
import os
import platform
import socket
import psutil
import pyautogui


# ==========================
# Time & Date
# ==========================

def get_time():
    return datetime.datetime.now().strftime("%I:%M:%S %p")


def get_date():
    return datetime.datetime.now().strftime("%A, %d %B %Y")


# ==========================
# Battery
# ==========================

def get_battery():

    battery = psutil.sensors_battery()

    if battery is None:
        return "❌ Battery information not available."

    status = "Charging ⚡" if battery.power_plugged else "Not Charging 🔋"

    return (
        f"🔋 Battery: {battery.percent}%\n"
        f"Status: {status}"
    )


# ==========================
# RAM
# ==========================

def get_ram():

    ram = psutil.virtual_memory()

    used = round(ram.used / (1024 ** 3), 2)
    total = round(ram.total / (1024 ** 3), 2)

    return f"💾 RAM Usage: {used} GB / {total} GB"


# ==========================
# CPU
# ==========================

def get_cpu():

    cpu = psutil.cpu_percent(interval=1)

    return f"🖥 CPU Usage: {cpu}%"


# ==========================
# PC Name
# ==========================

def get_pc_name():
    return socket.gethostname()


# ==========================
# Windows Version
# ==========================

def get_windows():

    return platform.platform()


# ==========================
# Screenshot
# ==========================

def take_screenshot():

    os.makedirs("screenshots", exist_ok=True)

    filename = datetime.datetime.now().strftime(
        "screenshots/%Y%m%d_%H%M%S.png"
    )

    image = pyautogui.screenshot()

    image.save(filename)

    return f"📸 Screenshot saved:\n{filename}"


# ==========================
# Shutdown
# ==========================

def shutdown_pc():

    os.system("shutdown /s /t 1")

    return "Shutting down..."


# ==========================
# Restart
# ==========================

def restart_pc():

    os.system("shutdown /r /t 1")

    return "Restarting..."


# ==========================
# Lock
# ==========================

def lock_pc():

    os.system("rundll32.exe user32.dll,LockWorkStation")

    return "🔒 PC Locked"


# ==========================
# Sleep
# ==========================

def sleep_pc():

    os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")

    return "😴 Going to sleep..."



import os


def system_commands(command):

    command = command.lower().strip()

    # ---------- INSTALL WIRESHARK ----------
    if "wireshark" in command and "install" in command:
        os.system("winget install --id WiresharkFoundation.Wireshark -e")
        return "🛠 Installing Wireshark..."

    # ---------- INSTALL NMAP ----------
    elif "nmap" in command and "install" in command:
        os.system("winget install --id Insecure.Nmap -e")
        return "🛠 Installing Nmap..."

    return None
# import datetime

# def get_time():
#     return datetime.datetime.now().strftime("%I:%M %p")


# def get_date():
#     return datetime.datetime.now().strftime("%d %B %Y")

