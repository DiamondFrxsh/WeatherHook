import json
import requests
import time
import os

version = '1.0.0'

previous_alerts = {}  # Store previous alert descriptions

coordsapi = "https://api.weather.gov/alerts/active?point="

def getAlerts(lat,long):
    response = requests.get(coordsapi + str(lat) + "," + str(long))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching alerts: {response.status_code}")
        return None

def getAlertInformation(alert_data):
    """
    Get alert information from all features in the alert data
    Returns a list of properties from all features found
    """
    if not alert_data or not isinstance(alert_data, dict):
        print("Invalid alert data received")
        return None
        
    try:
        print("Processing alert data...")
        if 'features' not in alert_data:
            print("No features found in alert data")
            return None
            
        features = alert_data['features']
        if not features:
            return None
            
        print(f"Found {len(features)} features")
        
        # Get properties from all features
        alert_properties = []
        for feature in features:
            if isinstance(feature, dict) and 'properties' in feature:
                alert_properties.append(feature['properties'])
        
        if alert_properties:
            return alert_properties
        
        print("No valid alert properties found")
        return None
            
    except Exception as e:
        print(f"Error processing alert: {str(e)}")
        print(f"Alert data structure: {json.dumps(alert_data, indent=2)}")
        return None

# Extract information from the save file (version, coordinates, and webhook URL)
with open(os.path.join(os.path.join(os.getcwd(), 'save'), 'save.json'), "r") as save_json:
    data = json.load(save_json)
latitude = data['latitude']
longitude = data['longitude']
webhook = data['webhookurl']

# Main loop to check for alerts
while True:
    print(f"Checking for alerts...")
    alerts = getAlerts(latitude, longitude)
    if alerts:
        print("Alerts found!")
        print("Getting alert information...")
        alert_infos = getAlertInformation(alerts)
        if alert_infos:
            print(f"Found {len(alert_infos)} alerts!")
            current_alerts = {}

            for alert_info in alert_infos:
                print("Checking alert updates...")
                alert_id = alert_info.get('id')
                description = alert_info.get('description', 'N/A')
                # Check if the alert is new or updated
                if alert_id not in previous_alerts or previous_alerts[alert_id] != description:
                    print(f"New or updated alert: {alert_info.get('event', 'N/A')}")
                    print("Building alert embed...")
                    alertData = {
                        "embeds": [
                            {
                                "title": alert_info.get('event', 'N/A'),
                                "description": alert_info.get('description', 'N/A'),
                                "color": 16711680,
                                "fields": [
                                    {
                                        "name": "Headline:",
                                        "value": alert_info.get('headline', 'N/A')
                                    }
                                ],
                                "footer": {"text": f"WeatherHook V{version}"}
                            }
                        ]
                    }
                    print("Sending alert...")
                    response = requests.post(webhook, json=alertData)
                    if response.status_code == 204:
                        print("Alert sent successfully!")
                    else:
                        print(f"Failed to send alert: {response.status_code}")
                else:
                    print(f"No new updates for this {alert_info.get('event', 'N/A')}.")
                # Store current alert in the dictionary
                current_alerts[alert_id] = description
            # Update previous_alerts with current alerts
            previous_alerts = current_alerts
        else:
            print("No alert information found")
    else:
        # Clear previous alerts if no active alerts are found
        if previous_alerts:
            print("Clearing expired alerts")
            previous_alerts.clear()
    print('Scanning again in 60 seconds...')
    time.sleep(60)  # Wait for 1 minute before checking again