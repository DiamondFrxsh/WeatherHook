import json
import requests
import sys
import os
import msvcrt
import shutil
import win32com.client

version = '1.0.0'

testData = {
    "content": "This is a test message from WeatherHook; you're all set up!"
}

def getcoordinatesfromzip(zipcode):
    try:
        response = requests.get(f"https://api.zippopotam.us/us/{zipcode}")
        if response.status_code == 200:
            data = response.json()
            return {
                'latitude': float(data['places'][0]['latitude']),
                'longitude': float(data['places'][0]['longitude'])
            }
        return None
    except:
        return None
    
def findvaluebykey(data, target_key):
    """
    Find the first value for a given key in nested data structures
    """
    if not data:
        return None

    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            if isinstance(value, (dict, list)):
                result = findvaluebykey(value, target_key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                result = findvaluebykey(item, target_key)
                if result is not None:
                    return result
    return None

def boot():
    if not os.path.isdir(os.path.join(os.getcwd(), "save")):
        setup()
    else:
        with open(os.path.join(os.path.join(os.getcwd(), 'save'), 'save.json'), "r") as save_json:
            data = json.load(save_json)
        if data["version"] != version:
            vermigrate()
        else:
            options()

def setup():
    print(str('Version ' + version))
    print('Welcome to WeatherHook!')
    print()
    print('This program is used to alert the user using a Discord webhook whenever an alert is issued in their area.')
    print("This only works with cities in the United States (for now). If you wanted to get updates for areas outside of the US, sorry!")
    print()
    print('DISCLAIMER: This program and its developer are NOT in any way affiliated with the National Weather Service, and I do not recommend using this as a primary way to receive warnings.')
    print('If you live in the United States and need a way to receive weather alerts, I highly recommend using the resources listed in the readme.')
    print()
    zipcode = input("First thing's first: enter the ZIP code for the area you want to receive alerts for: ")
    print('Checking ZIP code...')
    location = getcoordinatesfromzip(zipcode)
    if location:
        print('Location found!')
        webhookURL = input('Now, enter your Discord webhook URL: ')
        print('Checking URL...')
        try:
            response = requests.post(webhookURL, data=testData)
        except Exception as e:
            print(f'An error occurred while checking the URL: {e}')
            print('Press any key to quit:')
            msvcrt.getch()
            sys.exit()
        if response.status_code == 204:
            try:
                print('Discord webhook is set up!')
                print('Creating save directory...')
                os.mkdir('save')
                print('Save directory created!')
                print('Creating save file...')
                savedir = os.path.join(os.getcwd(), 'save')
                savename = 'save.json'
                savepath = os.path.join(savedir, savename)
                data = {"version": version, "latitude": float(findvaluebykey(location, "latitude")), "longitude": float(findvaluebykey(location, "longitude")), "webhookurl": webhookURL}
                with open(savepath, "w") as save_json:
                    json.dump(data, save_json, indent=4)
                print('Save file created!')
            except Exception as e:
                print(f'An error occurred while creating the save data: {e}')
                print('Press any key to quit:')
                msvcrt.getch()
                sys.exit()
            print('Optional: Would you like to set this program to run on startup? (y/n)')
            inputstart = input('Option chosen: ')
            if inputstart.lower() == 'y':
                try:
                    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
                    shortcut_path = os.path.join(startup_path, 'whclient.lnk')
                    target = os.path.join(os.getcwd(), 'whclient.exe')
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(shortcut_path)
                    shortcut.TargetPath = target
                    shortcut.WorkingDirectory = os.getcwd()
                    shortcut.save()
                    print('Shortcut created! WeatherHook will now run on startup or when you launch scan.exe. Press any key to quit:')
                    msvcrt.getch()
                    sys.exit()
                except Exception as e:
                    print(f'An error occurred while creating the startup shortcut: {e}')
                    print('Press any key to quit:')
                    msvcrt.getch()
                    sys.exit()
            elif inputstart.lower() == 'n':
                print('WeatherHook will not run on startup. You can change this in the options menu when you restart setup.exe. Press any key to quit:')
                msvcrt.getch()
                sys.exit()
            else:
                print('Invalid option. You can set this up in the options menu when you restart setup.exe. Press any key to quit:')
                msvcrt.getch()
                sys.exit()

    else:
        print('Invalid ZIP code. Press any key to quit:')
        msvcrt.getch()
        sys.exit()

def options():
    print(str('Version ' + version))
    print('WeatherHook Options')
    print('Hello! Choose an option below:')
    print('1: Install Startup     2: Uninstall     3: Quit')
    option = input('Option chosen: ')
    if option == "1":
        try:
            print('Installing to Startup...')
            startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            shortcut_path = os.path.join(startup_path, 'whclient.lnk')
            target = os.path.join(os.getcwd(), 'whclient.exe')
            shell = win32com.client.Dispatch("WScript.Shell")   
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target
            shortcut.WorkingDirectory = os.getcwd()
            shortcut.save()
            print('Shortcut created! WeatherHook will now run on startup or when you launch scan.exe. Press any key to quit:')
            msvcrt.getch()
            sys.exit()
        except Exception as e:
            print(f'An error occurred while creating the startup shortcut: {e}')
            print('Press any key to quit:')
            msvcrt.getch()
            sys.exit()

    elif option == "2":
        print('Uninstall Options:')
        print('What would you like to uninstall? Choose an option below:')
        print('1: Save Data     2: Startup')
        uninoption = input('Option chosen: ')
        if uninoption == "1":
            print('Deleting save directory...')
            shutil.rmtree(os.path.join(os.getcwd(), 'save'))
            print('Save data deleted! To set it up again, run this program. Press any key to quit:')
            msvcrt.getch()
            sys.exit()
        elif uninoption == "2":
            print('Deleting startup...')
            startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            shortcut_path = os.path.join(startup_path, 'whclient.lnk')
            if os.path.exists(shortcut_path):
                try:
                    os.remove(shortcut_path)
                    print('Startup shortcut deleted! WeatherHook will no longer run on startup. Press any key to quit:')
                    msvcrt.getch()
                    sys.exit()
                except Exception as e:
                    print(f'An error occurred while deleting the startup shortcut: {e}')
                    print('Press any key to quit:')
                    msvcrt.getch()
                    sys.exit()
            else:
                print('No startup shortcut found. WeatherHook will not run on startup. Press any key to quit:')
            print('Done! Press any key to quit...')
            msvcrt.getch()
            sys.exit()
        else:
            print('Invalid option. Press any key to quit...')
            msvcrt.getch()
            sys.exit()
    elif option == "3":
        print('Quitting...')
        sys.exit()
    else:
        print('Invalid option. Press any key to quit...')
        msvcrt.getch()
        sys.exit()

def vermigrate():
    print("Your save data does not have the same version as this program! Please follow the instructions below to fix it:")
    print("To make sure you get the best out of the program, you cannot downgrade your file's version. Please use a save with the same version as this program or download a newer version of the program. Press any key to quit:")
    msvcrt.getch()
    sys.exit()

boot()