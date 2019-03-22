import urllib.request
import json


def get_json():
    # get the json data from data.json
    with open("data.json", "r") as read_file:
        return json.load(read_file)["firmware"]


def get_git_info(repo):
    with urllib.request.urlopen("https://api.github.com/repos/" + repo) as url:
        return(json.loads(url.read().decode()))

def get_git_file_info(repo, file):
    with urllib.request.urlopen("https://api.github.com/repos/" + repo + "/contents/" + file) as url:
        return(json.loads(url.read().decode()))


def get_git_releases_info(repo):
    with urllib.request.urlopen("https://api.github.com/repos/" + repo + "/releases/latest") as url:
        return(json.loads(url.read().decode()))


def update_version(old_firmware):
    version = []
    # check if firmware is up to date
    # if version is not up to date start the update
    print("let's update")
    if old_firmware["name"] == "Tasmota":
        print("Tasmote update started")
        # Tasmota updater
        api_data = get_git_releases_info(old_firmware['repo'])
        for asset in api_data["assets"]:
            version.append({"name": asset["name"], "bin": [{"file": asset["name"], "ofset": "", "download": asset["browser_download_url"]}]})
        return version

    if old_firmware["name"] == "Sonoff Homekit":
        # Sonoff Homekit Updater
        print("Sonoff homekit update started")
        for version in old_firmware["versions"]:
            files = []
            versions = []
            for file in version["bin"]:
                file_data = get_git_file_info(old_firmware["repo"], old_firmware["update_settings"]["repo_path"] + file["file"])
                files.append({"file": old_firmware["name"], "ofset": file["ofset"], "download": file_data["download_url"], "sha": file_data["sha"]})
            versions.append(files)
        return(versions)

    elif old_firmware["name"] == "RavenCore":
        print("Ravencore update started")

    else:
        print("The auto updater does not support this firmware \n Old data will be used")

def update():
    data = get_json()
    new_data = {}
    new_data["firmware"] = []
    for firmware in data:
        print("updateting " + firmware["name"])
        # make all updates
        print("getting data from github api")
        info = get_git_info(firmware['repo'])
        print("data recieved")
        new_data["firmware"].append({"name": firmware["name"],
                                     "version": firmware["version"],
                                     "updated_at": firmware["updated_at"],
                                     "description": firmware["description"],
                                     "repo": "arendst/Sonoff-Tasmota",
                                     "stargazers_count": info["stargazers_count"],
                                     "forks_count": info["forks_count"],
                                     "license": info['license']['name'],
                                     "versions": update_version(firmware)})
    print("saving changes")
    with open('test_data.json', 'w') as outfile:
        json.dump(new_data, outfile, indent=4)
    print("changes saved to data.json")

if __name__ == '__main__':
    update()