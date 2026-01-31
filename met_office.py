from urllib import urequest
import gc
from ujson import load as json_load

import secrets

BASE_URL = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/"

# --- Met Office Site Specific Download ---
# > Based on https://github.com/MetOffice/weather_datahub_utilities/blob/main/site_specific_download/ss_download.py

def retrieve_forecast(timesteps, request_headers = {}, exclude_metadata = "FALSE", include_location = "TRUE"):
    headers = {
        "accept": "application/json",
        "apikey": secrets.MET_API_KEY,
        }
    headers.update(request_headers)
    
    params = {
        "excludeParameterMetadata"	: exclude_metadata,
        "includeLocationName"		: include_location,
        "latitude"					: secrets.HOME_LATITUDE,
        "longitude"					: secrets.HOME_LONGITUDE,
        }
    
    url = BASE_URL + timesteps
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
    "17": "Sleet Shower (Day)",
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

WEATHER_CODE_ICONS = {
    "NA": None,
    "-1": "wi-na",
    "0" : "wi-night-clear",
    "1" : "wi-day-sunny",
    "2" : "wi-night-alt-partly-cloudy",
    "3" : "wi-day-cloudy",
    "5" : "wi-na",  # Can't see a Mist entry in weather icons
    "6" : "wi-fog",
    "7" : "wi-cloudy",
    "8" : "wi-na",  # Can't see an Overcast entry in weather icons
    "9" : "wi-night-alt-showers",
    "10": "wi-day-showers",
    "11": "wi-showers",  # Drizzle
    "12": "wi-showers",  # Light rain
    "13": "wi-night-alt-rain",
    "14": "wi-day-rain",
    "15": "wi-rain",
    "16": "wi-night-alt-sleet",
    "17": "wi-day-sleet",
    "18": "wi-sleet",
    "19": "wi-night-alt-hail",
    "20": "wi-day-hail",
    "21": "wi-hail",
    "22": "wi-night-alt-snow",
    "23": "wi-day-snow",
    "24": "wi-snow",
    "25": "wi-snowflake-cold",  # Heavy snow night
    "26": "wi-snowflake-cold",  # Heavy snow day
    "27": "wi-snowflake-cold",  # Heavy snow neutral
    "28": "wi-night-alt-storm-showers",
    "29": "wi-day-storm-showers",
    "30": "wi-thunderstorm",
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
