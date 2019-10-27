import pyowm
import json
import time
import datetime
import RPi.GPIO as GPIO
from io import open

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.OUT)
GPIO.output(2, False)

now = datetime.now()

def rain_delay(retrieved_rain, how_long, off, start_time, retreived_rain):
    if off == "True":
        print("Device is OFF")
    elif retrieved_rain != "None":
        print("Rain forecasted. Skipping watering...")
    elif retreived_rain == "None" and now.strftime("%I:%M %p") == start_time:
        print("Starting Watering")
        GPIO.output(2, True)
        time.sleep(how_long)
        GPIO.output(1, False)
    else:
        print("Will start watering at" + start_time)


# Authenticates API Call
owm = pyowm.OWM('656b8099cafddbb09335cdab3e61ea7e')

# Defines print statement variables
obs = owm.weather_at_place('Redmond,US')
w = obs.get_weather()

# Print statement variables use
dict_temp = w.get_temperature('fahrenheit')
dict_temp = w.get_temperature('fahrenheit')
retrieved_temp = str(dict_temp.get('temp'))
dict_rain = w.get_rain()
retrieved_rain = str(dict_rain.get('3h'))

# Print calls
print(retrieved_rain)
print(retrieved_temp)

# Converts text to a python dictionary
with open("home/pi/config.json", 'r', encoding='utf-8-sig') as json_file:
    data = json_file.read()
    dict_data = json.loads(data)
    off = dict_data.get("off")
    how_long = dict_data.get("how_long")
    start_time = dict_data.get("start_time")
    how_often = dict_data.get("how_often")

# Prints dictionary
print(off)
print(dict_data)
print(how_long)
print('Manual start time is', start_time)
print('System time:', now.strftime("%I:%M %p"))

# Calls Rain_delay defintion
rain_delay(retrieved_rain, off, how_long, start_time, retrieved_rain)
print("Watering Stopped")
