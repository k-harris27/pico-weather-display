import inky_frame
from picographics import \
    PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY
GRAPHICS = PicoGraphics(DISPLAY)

import met_office
import date
import read_bmp

TEXT_SCALE_LARGE = 8
TEXT_SCALE_MEDIUM = 4
TEXT_SCALE_SMALL = 2
TEXT_SIZE_Y = 8

BIG_STATS_X_LEFT = 200
BIG_STATS_Y_TOP  = 40
BIG_STATS_X_SEP  = 160
BIG_STATS_Y_SEP  = 90
BIG_STATS_ICON_Y = 10
BIG_STATS_ICON_WIDTH = 50

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

    GRAPHICS.set_pen(inky_frame.RED)
    _draw_text_right_justified(day_str, X_RIGHT_ANCHOR, 10, scale=TEXT_SCALE_LARGE)
    GRAPHICS.set_pen(inky_frame.BLACK)
    _draw_text_right_justified(date_str, X_RIGHT_ANCHOR, 20+TEXT_SIZE_Y*TEXT_SCALE_LARGE, scale=TEXT_SCALE_MEDIUM)

def _draw_today_overview(data_today):
    """
    Draw the overall data for today - numbers and large weather icon.
    
    :param data_today: Today's data json from the MET office daily timeseries.
    """
    
    # TODO: Check if we are within sunrise/sunset to choose day/night versions?
    _draw_weather_icon(data_today["daySignificantWeatherCode"], 20, 0)

    # --- Temperature ---
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/wi-thermometer-exterior_50x50.bmp", BIG_STATS_X_LEFT, BIG_STATS_Y_TOP+BIG_STATS_ICON_Y)
    GRAPHICS.set_pen(inky_frame.RED)
    read_bmp.draw(GRAPHICS, "bmp/wi-thermometer-internal_50x50.bmp", BIG_STATS_X_LEFT, BIG_STATS_Y_TOP+BIG_STATS_ICON_Y)
    GRAPHICS.set_pen(inky_frame.BLACK)

    max_temp = data_today["dayMaxScreenTemperature"]
    feels_like = data_today["dayMaxFeelsLikeTemp"]
    max_temp_str = f"{max_temp:02d}"
    max_temp_text_x = BIG_STATS_X_LEFT+BIG_STATS_ICON_WIDTH
    max_temp_text_x_right = max_temp_text_x + GRAPHICS.measure_text(max_temp_str, TEXT_SCALE_LARGE)
    GRAPHICS.text(f"{max_temp:02d}",
                  max_temp_text_x, BIG_STATS_Y_TOP,
                  scale=TEXT_SCALE_LARGE)
    GRAPHICS.text("°C", 
                  max_temp_text_x_right, BIG_STATS_Y_TOP, 
                  scale=TEXT_SCALE_MEDIUM)
    GRAPHICS.text(f"Feels like {feels_like}°C", 
                  max_temp_text_x, BIG_STATS_Y_TOP+TEXT_SCALE_LARGE*TEXT_SIZE_Y, 
                  scale=TEXT_SCALE_SMALL)


    # --- Precipitation ---
    column_2_x = BIG_STATS_X_LEFT+BIG_STATS_X_SEP
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/wi-umbrella_50x50.bmp", column_2_x, BIG_STATS_Y_TOP+BIG_STATS_ICON_Y)
    rain_chance = data_today["ChanceOfPrecipitation"]  # It's probably not this but something similar...
    rain_chance_text_x = column_2_x + BIG_STATS_ICON_WIDTH
    rain_chance_units_x = rain_chance_text_x + GRAPHICS.measure_text(str(rain_chance), TEXT_SCALE_LARGE)
    GRAPHICS.text(str(rain_chance),
                  rain_chance_text_x, BIG_STATS_Y_TOP,
                  scale=TEXT_SCALE_LARGE)
    GRAPHICS.text("%",
                  rain_chance_units_x, BIG_STATS_Y_TOP,
                  scale=TEXT_SCALE_MEDIUM)
    

    # --- Wind ---
    row_2_y_top = BIG_STATS_Y_TOP+BIG_STATS_Y_SEP
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/wi-strong-wind_50x50.bmp", BIG_STATS_X_LEFT, row_2_y_top+BIG_STATS_ICON_Y)
    wind_speed = data_today["WhateverWindSpeedIs"]
    wind_speed_text_x = BIG_STATS_X_LEFT+BIG_STATS_ICON_WIDTH
    wind_speed_units_x = wind_speed_text_x+GRAPHICS.measure_text(str(wind_speed), TEXT_SCALE_LARGE)
    GRAPHICS.text(str(wind_speed),
                  wind_speed_text_x, row_2_y_top,
                  scale=TEXT_SCALE_LARGE)
    GRAPHICS.text("mph",
                  wind_speed_units_x, row_2_y_top,
                  scale=TEXT_SCALE_SMALL)
    
    ## TODO: Arrow for direction of wind speed
    

def _draw_weather_icon(weather_code, x, y):
    """
    Draw the bitmap icon corresponding to weather_code with the top left at (x,y) 
    
    :param weather_code: int MET office weather code (see met_office.py for values)
    :param x: int x position of left side of icon
    :param y: int y position of top side of icon
    """

    icon_name = met_office.WEATHER_CODE_ICONS[str(weather_code)]
    icon_path = "/bmp/" + icon_name + ".bmp"
    GRAPHICS.set_pen(inky_frame.BLUE)
    read_bmp.draw(GRAPHICS, icon_path, x, y)

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