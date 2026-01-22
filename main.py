import micropython
import gc
import time
from urllib import urequest
from ujson import load as json_load

from machine import Pin
import inky_frame
from picographics import \
     PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY

# --- TEST Met Office Site Specific Download ---
# > Based on https://github.com/MetOffice/weather_datahub_utilities/blob/main/site_specific_download/ss_download.py

BASE_URL = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/"

import secrets

GRAPHICS = PicoGraphics(DISPLAY)

def main():
    weather_json = retrieve_forecast(
        BASE_URL,
        timesteps = "hourly",
        latitude = secrets.HOME_LATITUDE,
        longitude = secrets.HOME_LONGITUDE,
        )
    location = weather_json["location"]["name"]
    timeseries = weather_json["timeSeries"]
    
    print("Debug:")
    for k,v in timeseries[0].items():
        print(f"{k}: {v}")
    
    draw_weather(location, timeseries)
    

def draw_weather(location, timeseries):
    GRAPHICS.set_pen(inky_frame.WHITE)
    GRAPHICS.clear()
    GRAPHICS.set_pen(inky_frame.BLACK)
    GRAPHICS.set_font("bitmap8")
    
    data_now = timeseries[0]
    weather_text = WEATHER_CODES[str(data_now["significantWeatherCode"])]
    temperature = int(float(data_now["screenTemperature"]))
    feels_like = int(float(data_now["feelsLikeTemperature"]))
    rain_chance = float(data_now["probOfPrecipitation"])
    
    _TEXT_SEP = 60
    
    GRAPHICS.text(f"Location: 		{location}", 0, 0, 600, 4)
    GRAPHICS.text(f"Weather:  		{weather_text}", 0, _TEXT_SEP, 600, 4)
    GRAPHICS.text(f"Temperature: 	{temperature}", 0, 2*_TEXT_SEP, 600, 4)
    GRAPHICS.text(f"Feels Like: 	{feels_like}", 0, 3*_TEXT_SEP, 600, 4)
    GRAPHICS.text(f"Chance of Rain: {rain_chance}", 0, 4*_TEXT_SEP, 600, 4)
    
    GRAPHICS.update()

def _OLD():
    GRAPHICS.set_pen(inky_frame.WHITE)
    GRAPHICS.clear()
    GRAPHICS.set_pen(inky_frame.BLACK)
    GRAPHICS.set_font('bitmap8')
    GRAPHICS.text("Hello Inky", 0, 0, 600, 4)
    GRAPHICS.update()

    while True:
        if inky_frame.button_a.is_pressed:
            inky_frame.button_a.led_on()
        else:
            inky_frame.button_a.led_off()

def retrieve_forecast(base_url, timesteps, latitude, longitude, request_headers = {}, exclude_metadata = "FALSE", include_location = "TRUE"):
    headers = {
        "accept": "application/json",
        "apikey": secrets.MET_API_KEY,
        }
    headers.update(request_headers)
    
    params = {
        "excludeParameterMetadata"	: exclude_metadata,
        "includeLocationName"		: include_location,
        "latitude"					: latitude,
        "longitude"					: longitude,
        }
    
    url = base_url + timesteps
    url = encode_url(url, params)
    
    retries = 5
    jdata = {}
    
    for _ in range(retries):
        socket = urequest.urlopen(
            url = url,
            headers = headers,
            )
        gc.collect()
        jdata = json_load(socket)
        socket.close()
        gc.collect()
        try:
            return jdata["features"][0]["properties"]
        except KeyError as e:
            print("Connection error:")
            for k, v in jdata.items():
                print(f"\t{k}: {v}")
            print("Retrying...\n")
    return jdata

def encode_url(base_url, params = {}):
    param_str = "&".join(f"{k}={v}" for k,v in params.items())
    return base_url + "?" + param_str


# --- Code definitions ---
# https://www.metoffice.gov.uk/services/data/datapoint/code-definitions

WEATHER_CODES = {
    "NA": "Not Available",
    "-1": "Trace Rain",
    "0" : "Clear Night",
    "1" : "Sunny Day",
    "2" : "Partly Cloudy (Night)",
    "3" : "Partly Cloudy (Day)",
    "5" : "Mist",
    "6" : "Fog",
    "7" : "Cloudy",
    "8" : "Overcast",
    "9" : "Light Rain Shower (Night)",
    "10": "Light Rain Shower (Day)",
    "11": "Drizzle",
    "12": "Light Rain",
    "13": "Heavy Rain Shower (Night)",
    "14": "Heavy Rain Shower (Day)",
    "15": "Heavy Rain",
    "16": "Sleet Shower (Night)",
    "17": "Sleep Shower (Day)",
    "18": "Sleet",
    "19": "Hail Shower (Night)",
    "20": "Hail Shower (Day)",
    "21": "Hail",
    "22": "Light Snow Shower (Night)",
    "23": "Light Snow Shower (Day)",
    "24": "Light Snow",
    "25": "Heavy Snow Shower (Night)",
    "26": "Heavy Snow Shower (Day)",
    "27": "Heavy Snow",
    "28": "Thunder Shower (Night)",
    "29": "Thunder Shower (Day)",
    "30": "Thunder",
    }

VIS_CODES = {
    "UN": "Unknown",
    "VP": "Very Poor",
    "PO": "Poor",
    "MO": "Moderate",
    "GO": "Good",
    "VG": "Very Good",
    "EX": "Excellent",
    }

main()
                
