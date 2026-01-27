
month_codes = [0, 3, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5]
days_of_week = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]

def day_of_week_from_date(year, month, day):
    """
    Return a string of the day of week based on numerical year, month and day of month.

    Based on https://artofmemory.com/blog/how-to-calculate-the-day-of-the-week/
    
    :param year: int
    :param month: int
    :param day: int
    """

    year_last_two = year % 100
    year_code = (year_last_two + (year_last_two // 4)) % 7

    month_code = month_codes[month-1]

    century_code = 6  # Will break in 2100.

    leap_year_code = 0
    if month < 3: 
        # Leap year code only applies if the month is Jan or Feb.
        # TODO: Needs checking
        is_leap_year = (year % 400 == 0) or (year % 4 == 0 and not year % 100 == 0)
        leap_year_code -= int(is_leap_year)

    day_of_week = (year_code + month_code + century_code + day - leap_year_code) % 7
