import inky_frame
from picographics import \
     PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY

import met_office
import date

TEXT_SCALE_LARGE = 8
TEXT_SCALE_MEDIUM = 4
TEXT_SCALE_SMALL = 2

GRAPHICS = PicoGraphics(DISPLAY)

def draw_weather(location, timeseries):
    GRAPHICS.set_pen(inky_frame.WHITE)
    GRAPHICS.clear()
    GRAPHICS.set_pen(inky_frame.BLACK)
    GRAPHICS.set_font("bitmap8")
    
    data_now = timeseries[1]
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

    _draw_date(data_now["time"])
    
    GRAPHICS.update()

def _draw_date(time_str):
    """
    Draw the region displaying the day and date (currently top right).
    
    :param time_str: Time string received from MET office API.
    """
    
    X_RIGHT_ANCHOR = _x_from_right(10)

    year, month, day = date.date_from_time_str(time_str)
    day_str = date.day_of_week_from_date(year, month, day)
    month_str = date.get_month_3str(month)
    date_str = f"{year:04d} {month_str} {day:02d}"

    _draw_text_right_justified(day_str, X_RIGHT_ANCHOR, 10, scale=TEXT_SCALE_LARGE)
    _draw_text_right_justified(date_str, X_RIGHT_ANCHOR, 20+8*TEXT_SCALE_LARGE, scale=TEXT_SCALE_MEDIUM)


def _draw_text_right_justified(text, right_anchor, top_anchor, scale, spacing=1, fixed_width=False, **kwargs):
    """
    Draw right-justified text. Wraps GRAPHICS.text, which all kwargs are passed on to.
    
    :param text: str text to display
    :param right_anchor: int right-side position of text
    :param top_anchor: int top-side position of text
    :param scale: int scale of text
    :param spacing: int spacing between characters
    :param fixed_width: bool should characters have a fixed width
    :param kwargs: kwargs dict passed on to GRAPHICS.text
    """

    text_width = GRAPHICS.measure_text(text, scale, spacing, fixed_width)
    left_pos = right_anchor - text_width
    GRAPHICS.text(text, left_pos, top_anchor, scale=scale, spacing=spacing, fixed_width=fixed_width, **kwargs)

def _x_from_right(dist):
    """
    Return the x position `dist` from the right
    
    :param dist: int
    """
    return GRAPHICS.get_bounds()[0] - dist

def _y_from_bottom(dist):
    """
    Return the y position `dist` from the bottom
    
    :param dist: int
    """
    return GRAPHICS.get_bounds()[1] - dist