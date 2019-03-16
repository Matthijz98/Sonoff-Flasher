import urllib.request
import json

url = "https://api.github.com/repos/arendst/Sonoff-Tasmota/releases/latest"


def get_json():
    with open("data.json", "r") as read_file:
        return json.load(read_file)["firmware"]


def update_json():
    with open("data.json", "r") as jsonFile:
        old_data = json.load(jsonFile)

    tmp = old_data["location"]
    data["location"] = "NewPath"

    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)


def get_git_info(repo):
    with urllib.request.urlopen("https://api.github.com/repos/" + repo) as url:
        return(json.loads(url.read().decode()))


if __name__ == '__main__':
    data = get_json()

    for filmware in data:
        info = get_git_info(filmware['repo'])
        filmware
        print(info["stargazers_count"], info["forks_count"], info['license']['name'])