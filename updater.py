import urllib.request
import json

url = "https://api.github.com/repos/arendst/Sonoff-Tasmota/releases/latest"


with urllib.request.urlopen(url) as url:
    data = json.loads(url.read().decode())
    for release in data["assets"]:
        print("{\"name\": \""+release["name"]+"\",\"bin\": [{\"file\": \""+release["name"]+"\", \"ofset\": \"\", \"download\": \""+release["browser_download_url"]+"\"}]},")
