import requests
import json
import datetime
import time
import serial


def get_api_data():
    api_url = 'https://api.forecast.io/forecast/a203529c7e9e621d51937f726499e3f7/40.719453,-73.999942'
    res = requests.get(api_url)

    if res.status_code == 200:
        return json.loads(res.content)


def get_rain_status(data):
    rain_status = False

    if data['currently']['precipIntensity'] > 0 or data['currently']['precipProbability'] > 0:
        rain_status = True
    
    hourly_data = data['hourly']['data'][:12]

    if will_rain(hourly_data):
        rain_status = True
    
    return rain_status


def will_rain(hourly_data):
    for item in hourly_data:
        if item['precipProbability'] > 0:
            return True
    return False


def main_loop():
    last_checked = datetime.datetime.now()
    current_time = datetime.datetime.now()
    data = get_api_data()
    ser = serial.Serial('/dev/tty.usbserial', 9600)
    
    while true:
        # prase output
        ser_output = ser.readline()
        
        person_nearby = None
        if person_nearby:
            flag = get_rain_status(data)
            ser.write('True')
            
        time.sleep(1)
        
        current_time = datetime.datetime.now()
        time_elapsed = last_checked - time_elasped

        diff = last_checked - current_time
        if diff.total_seconds() < -1800:
            # refresh api data
            data = get_api_data()
            last_checked = datetime.datetime.now()


main_loop()
