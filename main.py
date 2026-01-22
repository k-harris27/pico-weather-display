import network
import inky_frame
from picographics import \
     PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY

import met_office
import inky_helper

GRAPHICS = PicoGraphics(DISPLAY)

def main():

    check_network_connection()

    weather_json = met_office.retrieve_forecast(
        timesteps = "hourly",
        )
    location = weather_json["location"]["name"]
    timeseries = weather_json["timeSeries"]
    
    print("Debug:")
    for k,v in timeseries[0].items():
        print(f"{k}: {v}")
    
    draw_weather(location, timeseries)
    
def check_network_connection():
    """
    A network connection should be automatically started by the firmware when the pico starts.
    It can fail for unexpected reasons (such as state.json not existing). In this case, we can connect manually.
    """
    wlan = network.WLAN(network.WLAN.IF_STA)
    if not wlan.active():
        import secrets
        inky_helper.network_connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

def draw_weather(location, timeseries):
    GRAPHICS.set_pen(inky_frame.WHITE)
    GRAPHICS.clear()
    GRAPHICS.set_pen(inky_frame.BLACK)
    GRAPHICS.set_font("bitmap8")
    
    data_now = timeseries[0]
    weather_text = met_office.WEATHER_CODES[str(data_now["significantWeatherCode"])]
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

main()
                
