from urllib import urequest
import gc
from ujson import load as json_load

import secrets

BASE_URL = f"https://api.open-meteo.com/v1/forecast?latitude={secrets.HOME_LATITUDE}&longitude={secrets.HOME_LONGITUDE}"+\
            "&daily=weather_code,temperature_2m_max,apparent_temperature_max,uv_index_max,sunrise,sunset,precipitation_probability_max,wind_speed_10m_max"+\
            "&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers"+\
            "&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,weather_code,cloud_cover,precipitation,rain,showers,snowfall&timezone=auto"+\
            "&timeformat=unixtime&wind_speed_unit=mph&forecast_hours=24"
AIR_QUALITY_URL = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={secrets.HOME_LATITUDE}&longitude={secrets.HOME_LONGITUDE}"+\
                   "&current=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen&timezone=auto"

def retrieve_forecast():
    weather_json = _retrieve_weather()
    air_quality_json = _retrieve_air_quality()
    weather_json["current"]["pollen"] = air_quality_json
    return weather_json

def _retrieve_weather():
    retries = 5
    jdata = {}
    
    for _ in range(retries):
        socket = urequest.urlopen(
            url = BASE_URL,
            )
        gc.collect()
        jdata = json_load(socket)
        socket.close()
        gc.collect()
        try:
            return jdata
        except KeyError as e:
            print("Connection error:")
            for k, v in jdata.items():
                print(f"\t{k}: {v}")
            print("Retrying...\n")
    return jdata

def _retrieve_air_quality():
    retries = 5
    jdata = {}
    
    for _ in range(retries):
        socket = urequest.urlopen(
            url = AIR_QUALITY_URL,
            )
        gc.collect()
        jdata = json_load(socket)
        socket.close()
        gc.collect()
        try:
            return jdata["current"]
        except KeyError as e:
            print("Connection error:")
            for k, v in jdata.items():
                print(f"\t{k}: {v}")
            print("Retrying...\n")
    return jdata

def pollen_counts_to_rating(pollen_counts):
    """
    Convert pollen counts to a rating Low, Medium, High or Very High
    based on https://www.allergyclinic.co.uk/blog/pollen-count-uk-how-to-read-forecast-for-your-area
    
    :param pollen_counts: list of pollen counts from the API
    :return: Pollen rating string
    """
    max_count = max(pollen_counts)
    if max_count < 30:
        return "Low"
    elif max_count < 50:
        return "Med"
    elif max_count < 150:
        return "Hi"
    else:
        return "VHi"

# --- Code Definitions ---
WEATHER_CODES = {
    "0": "Clear sky",
    "1": "Mainly clear",
    "2": "Partly cloudy",
    "3": "Overcast",
    "45": "Fog",
    "48": "Depositing rime fog",
    "51": "Light drizzle",
    "53": "Moderate drizzle",
    "55": "Dense drizzle",
    "56": "Light freezing drizzle",
    "57": "Dense freezing drizzle",
    "61": "Slight rain",
    "63": "Moderate rain",
    "65": "Heavy rain",
    "66": "Light freezing rain",
    "67": "Heavy freezing rain",
    "71": "Slight snow fall",
    "73": "Moderate snow fall",
    "75": "Heavy snow fall",
    "77": "Snow grains",
    "80": "Slight rain showers",
    "81": "Moderate rain showers",
    "82": "Heavy rain showers",
    "85": "Slight snow showers",
    "86": "Heavy snow showers",
    "95": "Thunderstorm"
}

WEATHER_CODE_ICONS = {
    "0": "wi-day-sunny",
    "1": "wi-day-haze",
    "2": "wi-day-cloudy",
    "3": "wi-cloudy",
    "45": "wi-fog",
    "48": "wi-fog",
    "51": "wi-day-showers",
    "53": "wi-day-showers",
    "55": "wi-day-showers",
    "56": "wi-day-sleet",
    "57": "wi-day-sleet",
    "61": "wi-day-rain",
    "63": "wi-day-rain",
    "65": "wi-day-rain",
    "66": "wi-day-sleet",
    "67": "wi-day-sleet",
    "71": "wi-day-snow",
    "73": "wi-day-snow",
    "75": "wi-day-snow",
    "77": "wi-day-snow",
    "80": "wi-day-showers",
    "81": "wi-day-showers",
    "82": "wi-day-showers",
    "85": "wi-day-snow",
    "86": "wi-day-snow",
    "95": "wi-day-thunderstorm"
}