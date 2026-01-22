import inky_frame
from picographics import \
     PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY

import met_office

GRAPHICS = PicoGraphics(DISPLAY)

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
