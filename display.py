import inky_frame
from picographics import \
    PicoGraphics, DISPLAY_INKY_FRAME_SPECTRA_7 as DISPLAY
GRAPHICS = PicoGraphics(DISPLAY)

import open_meteo as weather_api
import time
import date
import read_bmp

TEXT_SCALE_LARGE = 8
TEXT_SCALE_MEDIUM = 4
TEXT_SCALE_SMALL = 2
TEXT_SIZE_Y = 8

BIG_STATS_X_LEFT = 200
BIG_STATS_Y_TOP  = 20
BIG_STATS_X_SEP  = 160
BIG_STATS_Y_SEP  = 110
BIG_STATS_ICON_Y = 0
BIG_STATS_ICON_WIDTH = 50
BIG_STATS_UNITS_OFFSET = 3

def draw_weather(json):
    GRAPHICS.set_pen(inky_frame.WHITE)
    GRAPHICS.clear()
    GRAPHICS.set_pen(inky_frame.BLACK)
    GRAPHICS.set_font("bitmap8")

    _draw_date(json["current"]["time"])

    _draw_today_overview(json)
    
    GRAPHICS.update()

def _draw_date(time_str):
    """
    Draw the region displaying the day and date (currently top right).
    
    :param time_str: Unix time string.
    """
    
    X_RIGHT_ANCHOR = _x_from_right(10)

    time_tuple = time.localtime(time_str)
    year, month, day = time_tuple[:3]
    weekday = (time_tuple[6] + 1) % 7  # Convert from 0=Mon to 0=Sun
    day_str = date.days_of_week[weekday]
    month_str = date.get_month_3str(month)
    date_str = f"{day:02d} {month_str} {year:04d}"

    GRAPHICS.set_pen(inky_frame.RED)
    _draw_text_right_justified(day_str, X_RIGHT_ANCHOR, 10, scale=TEXT_SCALE_MEDIUM)
    GRAPHICS.set_pen(inky_frame.BLACK)
    _draw_text_right_justified(date_str, X_RIGHT_ANCHOR, 20+TEXT_SIZE_Y*TEXT_SCALE_MEDIUM, scale=TEXT_SCALE_MEDIUM)

def _draw_today_overview(json):
    """
    Draw the overall data for today - numbers and large weather icon.
    
    :param json: weather json from the API.
    """
    
    data_current = json["current"]
    data_today = {key: timeseries[0] for key, timeseries in json["daily"].items()}
    
    # TODO: Check if we are within sunrise/sunset to choose day/night versions?
    _draw_weather_icon(data_current["weather_code"], 20, 0)

    # --- Temperature ---
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/wi-thermometer-exterior_50x50.bmp", BIG_STATS_X_LEFT, BIG_STATS_Y_TOP+BIG_STATS_ICON_Y)
    GRAPHICS.set_pen(inky_frame.RED)
    read_bmp.draw(GRAPHICS, "bmp/wi-thermometer-internal_50x50.bmp", BIG_STATS_X_LEFT, BIG_STATS_Y_TOP+BIG_STATS_ICON_Y)
    GRAPHICS.set_pen(inky_frame.BLACK)

    max_temp = round(data_current["temperature_2m"])
    feels_like = round(data_current["apparent_temperature"])
    max_temp_str = f"{max_temp:02d}"
    feels_like_str = f"{feels_like:02d}"
    max_temp_text_x = BIG_STATS_X_LEFT+BIG_STATS_ICON_WIDTH
    max_temp_text_x_right = max_temp_text_x + GRAPHICS.measure_text(max_temp_str, TEXT_SCALE_LARGE) + BIG_STATS_UNITS_OFFSET
    GRAPHICS.text(max_temp_str,
                  max_temp_text_x, BIG_STATS_Y_TOP,
                  scale=TEXT_SCALE_LARGE)
    GRAPHICS.text("°C", 
                  max_temp_text_x_right, BIG_STATS_Y_TOP, 
                  scale=TEXT_SCALE_MEDIUM)
    GRAPHICS.text(f"Feels like {feels_like_str}°C", 
                  BIG_STATS_X_LEFT, BIG_STATS_Y_TOP+TEXT_SCALE_LARGE*TEXT_SIZE_Y, 
                  scale=TEXT_SCALE_SMALL)

    # --- Precipitation ---
    column_2_x = BIG_STATS_X_LEFT+BIG_STATS_X_SEP
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/wi-umbrella_50x50.bmp", column_2_x, BIG_STATS_Y_TOP+BIG_STATS_ICON_Y)
    rain_chance = f"{data_today["precipitation_probability_max"]:02d}"
    current_rainfall = round(float(data_current["precipitation"])*10)/10
    rain_chance_text_x = column_2_x + BIG_STATS_ICON_WIDTH
    rain_chance_units_x = rain_chance_text_x + GRAPHICS.measure_text(rain_chance, TEXT_SCALE_LARGE) + BIG_STATS_UNITS_OFFSET
    GRAPHICS.text(rain_chance,
                  rain_chance_text_x, BIG_STATS_Y_TOP,
                  scale=TEXT_SCALE_LARGE)
    GRAPHICS.text("%",
                  rain_chance_units_x, BIG_STATS_Y_TOP,
                  scale=TEXT_SCALE_MEDIUM)
    GRAPHICS.text(f"Currently {current_rainfall} mm", 
                  column_2_x, BIG_STATS_Y_TOP+TEXT_SCALE_LARGE*TEXT_SIZE_Y, 
                  scale=TEXT_SCALE_SMALL)

    # --- Wind ---
    row_2_y_top = BIG_STATS_Y_TOP+BIG_STATS_Y_SEP
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/wi-strong-wind_50x50.bmp", BIG_STATS_X_LEFT, row_2_y_top+BIG_STATS_ICON_Y)
    wind_speed = f"{round(data_today["wind_speed_10m_max"]):02d}"
    wind_speed_text_x = BIG_STATS_X_LEFT+BIG_STATS_ICON_WIDTH
    wind_speed_units_x = wind_speed_text_x+GRAPHICS.measure_text(wind_speed, TEXT_SCALE_LARGE) + BIG_STATS_UNITS_OFFSET
    GRAPHICS.text(wind_speed,
                  wind_speed_text_x, row_2_y_top,
                  scale=TEXT_SCALE_LARGE)
    GRAPHICS.text("mph",
                  wind_speed_units_x, row_2_y_top,
                  scale=TEXT_SCALE_SMALL)
    
    ## TODO: Arrow for direction of wind speed
    
    # --- Pollen ---
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/flower_50x50.bmp", column_2_x, row_2_y_top+BIG_STATS_ICON_Y)
    pollen = weather_api.pollen_counts_to_rating([count for key, count in data_current["pollen"].items() if key.endswith("_pollen")])
    print([count for key, count in data_current["pollen"].items() if key.endswith("_pollen")])
    GRAPHICS.text(pollen,
                  column_2_x + BIG_STATS_ICON_WIDTH, row_2_y_top,
                  scale=TEXT_SCALE_LARGE)

    # --- UV Index ---
    pollen_extra_x = 30
    column_3_x = column_2_x+BIG_STATS_X_SEP+pollen_extra_x
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/wi-hot_50x50.bmp", column_3_x, row_2_y_top+BIG_STATS_ICON_Y)
    uv_index = f"{int(round(data_today["uv_index_max"])):01d}"
    GRAPHICS.text(uv_index,
                  column_3_x + BIG_STATS_ICON_WIDTH, row_2_y_top,
                  scale=TEXT_SCALE_LARGE)

    # --- Sunrise/Sunset ---
    uv_index_extra_x = -40
    column_4_x = column_3_x+BIG_STATS_X_SEP + uv_index_extra_x
    sunrise_y = row_2_y_top+BIG_STATS_ICON_Y-int(BIG_STATS_ICON_WIDTH//2.5)
    sunset_y = row_2_y_top+BIG_STATS_ICON_Y+int(BIG_STATS_ICON_WIDTH//2.5)
    text_offset_y = 10
    GRAPHICS.set_pen(inky_frame.BLACK)
    read_bmp.draw(GRAPHICS, "bmp/wi-sunrise_50x50.bmp", column_4_x, sunrise_y)
    read_bmp.draw(GRAPHICS, "bmp/wi-sunset_50x50.bmp", column_4_x, sunset_y)
    sunrise_time = time.localtime(data_today["sunrise"])
    sunrise_hour = f"{sunrise_time[3]:02d}"
    sunrise_minute = f":{sunrise_time[4]:02d}"
    sunrise_hour_width = GRAPHICS.measure_text(sunrise_hour, scale=TEXT_SCALE_MEDIUM)+5
    sunset_time = time.localtime(data_today["sunset"])
    sunset_hour = f"{sunset_time[3]:02d}"
    sunset_minute = f":{sunset_time[4]:02d}"
    sunset_hour_width = GRAPHICS.measure_text(sunset_hour, scale=TEXT_SCALE_MEDIUM)+5
    GRAPHICS.text(sunrise_hour,
                  column_4_x + BIG_STATS_ICON_WIDTH, sunrise_y + text_offset_y,
                  scale=TEXT_SCALE_MEDIUM)
    GRAPHICS.text(sunrise_minute,
                  column_4_x + BIG_STATS_ICON_WIDTH + sunrise_hour_width, sunrise_y + text_offset_y,
                  scale=TEXT_SCALE_SMALL)
    GRAPHICS.text(sunset_hour,
                  column_4_x + BIG_STATS_ICON_WIDTH, sunset_y + text_offset_y,
                  scale=TEXT_SCALE_MEDIUM)
    GRAPHICS.text(sunset_minute,
                  column_4_x + BIG_STATS_ICON_WIDTH + sunset_hour_width, sunset_y + text_offset_y,
                  scale=TEXT_SCALE_SMALL)
    
def _draw_weather_icon(weather_code, x, y):
    """
    Draw the bitmap icon corresponding to weather_code with the top left at (x,y) 
    
    :param weather_code: int MET office weather code (see met_office.py for values)
    :param x: int x position of left side of icon
    :param y: int y position of top side of icon
    """

    icon_name = weather_api.WEATHER_CODE_ICONS[str(weather_code)]
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