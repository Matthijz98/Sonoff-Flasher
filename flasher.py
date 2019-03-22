import os
import sys
import glob
import serial
import json
import wget
import updater

version = "0.0.0 alpha"
python_version = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[1])


def check_file_exists(filename):
    # return true if file exists in the data folder
    return os.path.isfile(os.getcwd() + "/data/" + filename)


def download_firmware(url):
    # use wget to download file to the data folde
    wget.download(url, os.getcwd() + "/data/")


def print_header(title):
    # the witdh of the header
    witdh = 55

    # small funtion to make a line of '*'
    def line():
        x = 0
        while x <= witdh:
            print("*", end="")
            x += 1

    # print the spaces needed
    def space(amount):
        x = 0
        while x <= amount:
            print(" ", end="")
            x += 1

    # this function is probably not needed but why not
    def calc():
        return int((witdh - len(title) - 2) / 2)

    # make the header
    line()
    print("\n*", end=""), space(calc()), print(title, end=""), space(calc()), print("*")
    line()
    print()


def start_screen():
    print_header("Welcome By Sonoff Flasher")
    print("\t \t Sonoff Flasher: " + version)
    print("\t \t Made by: Matthijz98")
    print("\t \t Python version: " + str(python_version))
    print("\t \t esptool.py version: ")
    print("\t \t COM PORTS detected: " + str(get_com_ports()))


def clear_screen():
    # clear the screen depending on the platform
    if sys.platform.startswith('win'):
        os.system('cls')
    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        os.system('clear')


def get_com_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def get_firmware_option():
    print_header("Choose a filmware")
    filmwares = get_json()
    choise = 0
    for filmware in filmwares:
        print("["+str(choise)+"]" + filmware["name"])
        choise += 1
    x = input("Select: ")
    return filmwares[int(x)]


def show_firmware_details(filmware):
    print_header(filmware['name'] + " details")
    print("Version: " + filmware["version"])
    print("Github URL: https://github.com/" + filmware["repo"])
    print("Description: " + filmware["description"])
    print("Verions:")
    for version in filmware['versions']:
        print("\t" + version['name'])


def get_json():
    with open("data.json", "r") as read_file:
        return json.load(read_file)["firmware"]


def flash(version, com):
    os.system("esptool.py -p "+com+" --baud 115200 write_flash -fs 8m -fm dout -ff 40m 0x0 " + version['bin'][0]["file"])
    #print("esptool.py -p "+com+" --baud 115200 write_flash -fs 8m -fm dout -ff 40m 0x0 " + version['bin'][0]["file"])


def show_and_get_options(options):
    choise = 0
    for option in options:
        print("[" + str(choise) + "]" + option + " ", end="")
        choise += 1
    return int(input("\nOption: "))


def update():
    clear_screen()
    print_header("Updater")
    print("This updater will update all the data in the data.json file using the Github api."
          "\nIMPORTANT NOTE: The open Github API has a limmit request of 60 request in a hour. "
          "\nThis updater requires less than that but please don't run this plugin multiple times in a hour"
          "\nIf you have custom changes made to the data.json make sure to backup them before proceeding")
    option = show_and_get_options(["next", "back"])
    clear_screen()
    if option == 0:
        print_header("Updater is running please wait")
        updater.update()
    elif option== 1:
        print("going back")

def get_firmware_version_option(filmware):
    x = 0
    for version in filmware["versions"]:
        print("[" + str(x) + "]" + version["name"] + " ")
        x += 1
    return filmware["versions"][int(input("Version:"))]


def wizzard(filmware):
    step = 0
    done = False
    while done is False:
        if step == 0:
            clear_screen()
            print_header("Let's Do This")
            print("Disclamer !!!!!! \nI'm in no way responsable for what you are going to do now, this software could break some things if someting goes wrong. Only if you are 100% sure that you can take the responabilty go to the next step.")
            x = show_and_get_options(["Next", "Stop"])
            if x == 1:
                break
            elif x == 0:
                step += 1
            else:
                break
        if step == 1:
            clear_screen()
            print_header("Please choose a version")
            filmware_version = get_firmware_version_option(filmware)
            step += 1
        if step == 2:
            clear_screen()
            print_header("Let's download all the file")
            for file in filmware_version["bin"]:
                print(file['file'])
                if check_file_exists(file['file']):
                    print("file already exists \n do you want to over write it?")
                    x = show_and_get_options(["yes", "no"])
                    if x == 0:
                        print("file will be overwritten")
                        download_firmware(file["download"])
                    if x == 1:
                        pass
                else:
                    download_firmware(file["download"])
            step += 1
        if step == 3:
            clear_screen()
            print_header("Let's flash that thing")
            flash(filmware_version, "COM5")
        if step == 4:
            clear_screen()
            print_header("Finished")
            input("pres any key to exit")
            done = True


if __name__ == '__main__':
    while True:
        clear_screen()
        start_screen()
        x = show_and_get_options(["Start", "Update", "Quit"])
        if x == 0:
            filmware = None
            while filmware != 0:
                clear_screen()
                filmware = get_firmware_option()
                clear_screen()
                show_firmware_details(filmware)
                x = show_and_get_options(["Choose", "View Github", "Go back"])
                if x == 0:
                    wizzard(filmware)
                    break
                if x == 1:
                    print()
                    break
                if x == 2:
                    print("back")
        if x == 1:
            update()
        if x == 2:
            sys.exit()

