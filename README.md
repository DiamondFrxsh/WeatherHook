# WeatherHook

WeatherHook is a simple application that checks for weather alerts concerning a specific area of the user's choice, and sends the information to a Discord webhook.

# Disclaimer:

This program and its developer are **NOT** in any way affiliated with the National Weather Service, and I do not recommend using this as a *primary* way to receive warnings. If you live in the United States and need a way to receive weather alerts, I highly recommend using the resources listed below:

- [Ready.gov](https://www.ready.gov/alerts) has information on several methods of receiving emergency alerts and how to set them up.
- For non-emergency alerts and weather forecasts, download a weather app like [The Weather Channel](https://weather.com/mission) or [AccuWeather](https://app.accuweather.com/app-download).

## Features

- Alert scanning
- Discord Webhook integration
- Yeah that's it

## Installation

1. Navigate to the latest release [here](https://github.com/DiamondFrxsh/WeatherHook/releases/latest)

2. Download the .zip file

3. Extract the files and run setup.exe

4. Follow the instructions and (optionally) install the program to the Startup folder
 
## Usage

The program will run automatically when the computer starts (if you chose to install to the Startup folder) or when you run whclient.exe

## How does it work?

WeatherHook works by first taking your ZIP code and converting it into a pair of latitude and longitude coordinates. Then, the coordinates are saved to the newly created save.json file along with the version number and webhook URL. Next, when whclient runs, the program calls [the National Weather Service's API](https://api.weather.gov) and queries for active alerts regarding the saved coordinates. The IDs of the active alerts are then searched through to find their information, like event types and descriptions. These values are returned to the program which relays the alert information to the saved Discord webhook. The process is then repeated every five seconds.

## License

This project is licensed under the MIT License (read LICENSE).