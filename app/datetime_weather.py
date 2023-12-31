import wifi
import socketpool
import rtc
import time
import board
import ssl
import os
import displayio
import terminalio
import adafruit_ntp
import adafruit_requests
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from utils import connect_wifi

font_15 = bitmap_font.load_font("fonts/Roboto-Regular-15.bdf")
font_21 = bitmap_font.load_font("fonts/Rubik-Medium-Numeric-21.bdf")
font_31 = bitmap_font.load_font("fonts/Roboto-Medium-31.bdf")
font_cn = bitmap_font.load_font("fonts/MaShanZheng-Regular-17.bdf")
weeks = ("MON","TUE","WED","THU","FRI","SAT","SUN")
UNITS = "metric"
REFRESH_SEC = 300

lcd = board.DISPLAY

print('         CLOCK  ')
print(' ')
print(' ')
print(' ')

connect_wifi()

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=8, server="asia.pool.ntp.org")
requests = adafruit_requests.Session(pool, ssl.create_default_context())

OWM_SOURCE = (
    "http://api.openweathermap.org/data/2.5/weather?q="
    + os.getenv("LOCATION")
    + "&units="
    + UNITS
    + "&mode=json"
    + "&appid="
    + os.getenv("OPENWEATHER_KEY")
)
LUNAR_SOURCE = "https://api.songzixian.com/api/perpetual-calendar?dataSource=local_perpetual_calendar&calendarType=gregorian"

try: 
    rtc.RTC().datetime = ntp.datetime
except Exception as e:
    print("RTC exception: ", e)
    pass
 
time_now = time.localtime()

date_label = label.Label(font_15, color=0x00ff00, scale=1)
date_label.anchor_point = (0.5, 0.0)
date_label.anchored_position = (lcd.width//2, 0)

time_label = label.Label(font_31, color=0x00ffff, scale=1)
time_label.anchor_point = (0.5, 0.0)
time_label.anchored_position = (lcd.width//2, 20)

lunar_label = label.Label(font_cn, color=0xffffff, scale=1)
lunar_label.anchor_point = (0.5, 0.0)
lunar_label.anchored_position = (lcd.width//2, 50)

image, palette = adafruit_imageload.load("/images/weather/icons8-sunny-32_.png")
palette.make_transparent(0)

tile_grid = displayio.TileGrid(image,pixel_shader = palette)
tile_grid.x = 0
tile_grid.y = 90

temp_label = label.Label(font_21, scale=1, color=0xffff00)
temp_label.anchor_point = (0.5, 0)
temp_label.anchored_position = (lcd.width -48,90)

description_label = label.Label(terminalio.FONT, scale=1, color=0xffff00)
description_label.anchor_point = (0.5, 0)
description_label.anchored_position = (lcd.width -48,110)

my_group = displayio.Group()
my_group.append(date_label)
my_group.append(time_label)
my_group.append(lunar_label)
my_group.append(tile_grid)
my_group.append(temp_label)
my_group.append(description_label)
lcd.root_group = my_group

def get_weather_condition_icon(weather_condition):
    if "cloud" in weather_condition.lower():
        return "/images/weather/icons8-cloudy-32_.png"
    elif "rain" in weather_condition.lower():
        return "/images/weather/icons8-rain-32_.png"
    elif "snow" in weather_condition.lower():
        return "/images/weather/icons8-snowy-32_.png"
    elif "clear" in weather_condition.lower():
        return "/images/weather/icons8-sunny-32_.png"
    else:
        return "/images/weather/icons8-sunny-32_.png"

def set_background(weather_condition, background_tile_grid):
    bitmap_path = get_weather_condition_icon(weather_condition)    
    image, palette = adafruit_imageload.load(bitmap_path)
    palette.make_transparent(0)
    background_tile_grid.bitmap = image
    background_tile_grid.pixel_shader = palette

def get_weather_data():
    print("Fetching json from", OWM_SOURCE)
    response = requests.get(OWM_SOURCE)
    print(response.json())

    current_temp = response.json()["main"]["temp"]
    current_weather_condition = response.json()["weather"][0]["main"]
    current_weather_description = response.json()["weather"][0]["description"]
    return current_temp,current_weather_condition, current_weather_description

def get_cn_date():
    print("Fetching json from", LUNAR_SOURCE)
    response = requests.get(LUNAR_SOURCE)
    print(response.json())
    nl = response.json()["data"]["lunarInfo"]["chineseDate"][5:]
    year = response.json()["data"]["traditionalChineseInfo"]["yearStemBranch"]
    return f"{year}{nl}"

current_temp,current_weather_condition, current_weather_description = get_weather_data()
lunar = get_cn_date()

start_time = time.monotonic()
start_day = time.localtime().tm_mday

while True:
    current_time = time.monotonic()
    print("Time DIFF:", current_time - start_time)
    if (current_time - start_time) > REFRESH_SEC:
        current_temp,current_weather_condition, current_weather_description = get_weather_data()
        start_time = current_time

    time_now = time.localtime()
    if time_now.tm_mday != start_day:
        lunar = get_cn_date()
        start_day = time_now.tm_mday
    week_id = time_now.tm_wday
    week = weeks[week_id]
    lunar_label.text = lunar
    date = "{:0>2d}/{:0>2d}/{:4d}".format(time_now.tm_mday,time_now.tm_mon,time_now.tm_year)
    date_label.text = f"{week}, {date}"
    time_label.text = "{:0>2d}:{:0>2d}:{:0>2d}".format(time_now.tm_hour,time_now.tm_min,time_now.tm_sec)
    description_label.text = current_weather_description
    temp_label.text = "{:.1f} °C".format(current_temp)
    set_background(current_weather_condition, tile_grid)

    time.sleep(1)