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
