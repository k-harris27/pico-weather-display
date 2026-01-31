import inky_frame
from picographics import \
     PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY

import met_office
import date
import read_bmp

TEXT_SCALE_LARGE = 8
TEXT_SCALE_MEDIUM = 4
TEXT_SCALE_SMALL = 2

GRAPHICS = PicoGraphics(DISPLAY)

def draw_weather(location, hourly_timeseries, daily_timeseries):
    GRAPHICS.set_pen(inky_frame.WHITE)
    GRAPHICS.clear()
    GRAPHICS.set_pen(inky_frame.BLACK)
    GRAPHICS.set_font("bitmap8")
    
    data_today = daily_timeseries[1]  # First daily entry is yesterday

    _draw_date(data_today["time"])

    _draw_today_overview(data_today)
    
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

def _draw_today_overview(data_today):
    """
    Draw the overall data for today - numbers and large weather icon.
    
    :param data_today: Today's data json from the MET office daily timeseries.
    """
    
    # TODO: Check if we are within sunrise/sunset to choose day/night versions?
    _draw_weather_icon(data_today["daySignificantWeatherCode"], 20, 20)

def _draw_weather_icon(weather_code, x, y):
    """
    Draw the bitmap icon corresponding to weather_code with the top left at (x,y) 
    
    :param weather_code: int MET office weather code (see met_office.py for values)
    :param x: int x position of left side of icon
    :param y: int y position of top side of icon
    """

    icon_name = met_office.WEATHER_CODE_ICONS[str(weather_code)]
    icon_path = "/bmp/" + icon_name + ".bmp"
    bmp_reader = read_bmp.gen_pixels(icon_path)
    width, height = next(bmp_reader)  # First yield gives width and height. All others give pixel info.
    y_lower_edge = y + height
    GRAPHICS.set_pen(inky_frame.BLACK)
    print("WARNING: bitmap reading currently only supports drawn or transparent (alpha channel) since the display has just 7 colours.")
    for n, pixel_data in enumerate(bmp_reader):
        # Skip transparent pixels
        if len(pixel_data) > 3 and pixel_data[3] == 0:
            continue
        pixel_x = x + n % width
        pixel_y = y_lower_edge - n // width
        GRAPHICS.rectangle(pixel_x, pixel_y, 1, 1)

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