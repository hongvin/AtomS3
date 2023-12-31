import os
import wifi
import time
import socketpool
import board
import ssl
import displayio
import terminalio
import adafruit_requests
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
from utils import connect_wifi

font_file = "fonts/Rubik-Medium-Numeric-21.bdf"
font = bitmap_font.load_font(font_file)
UNITS = "metric"

lcd = board.DISPLAY

print('         Weather  ')
print(' ')
print(' ')
print(' ')

connect_wifi()

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

DATA_SOURCE = (
    "http://api.openweathermap.org/data/2.5/weather?q="
    + os.getenv("LOCATION")
    + "&units="
    + UNITS
    + "&mode=json"
    + "&appid="
    + os.getenv("OPENWEATHER_KEY")
)

time_interval = 3000  

image, palette = adafruit_imageload.load("/images/weather/icons8-sunny-64_.png")
palette.make_transparent(0)

tile_grid = displayio.TileGrid(image,pixel_shader = palette)
tile_grid.x = lcd.width // 2 - tile_grid.tile_width // 2
tile_grid.y = lcd.height // 2 - tile_grid.tile_height // 2 - 12

group = displayio.Group()
group.append(tile_grid)

# Create label for displaying temperature data
text_area = bitmap_label.Label(font, scale=1)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (lcd.width // 2, lcd.height - 15)

location_label = bitmap_label.Label(terminalio.FONT, scale=1, color=0x00ffff)
location_label.anchor_point = (0.5, 0.5)
location_label.anchored_position = (lcd.width // 2, 8)
location_label.text=os.getenv("LOCATION")

description_label = bitmap_label.Label(terminalio.FONT, scale=1, color=0x00ff00)
description_label.anchor_point = (0.5, 0.5)
description_label.anchored_position = (lcd.width // 2, lcd.height // 2 +25)

# Create main group to hold all display groups
main_group = displayio.Group()
main_group.append(group)
main_group.append(location_label)
main_group.append(description_label)
main_group.append(text_area)
# Show the main group on the display
lcd.root_group = main_group

# Define function to get the appropriate weather icon
def get_weather_condition_icon(weather_condition):
    if "cloud" in weather_condition.lower():
        return "/images/weather/icons8-cloudy-64_.png"
    elif "rain" in weather_condition.lower():
        return "/images/weather/icons8-rain-64_.png"
    elif "snow" in weather_condition.lower():
        return "/images/weather/icons8-snowy-64_.png"
    elif "clear" in weather_condition.lower():
        return "/images/weather/icons8-sunny-64_.png"
    else:
        return "/images/weather/icons8-sunny-64_.png"

# Define function to update the background image based on weather conditions
def set_background(weather_condition, background_tile_grid):
    bitmap_path = get_weather_condition_icon(weather_condition)    
    image, palette = adafruit_imageload.load(bitmap_path)
    palette.make_transparent(0)
    background_tile_grid.bitmap = image
    background_tile_grid.pixel_shader = palette

while True:

    # Fetch weather data from OpenWeatherMap API
    print("Fetching json from", DATA_SOURCE)
    response = requests.get(DATA_SOURCE)
    print(response.json())

    # Extract temperature and weather condition data from API response
    current_temp = response.json()["main"]["temp"]
    max_temp = response.json()["main"]["temp_max"]
    min_temp = response.json()["main"]["temp_min"]
    current_weather_condition = response.json()["weather"][0]["main"]
    current_weather_description = response.json()["weather"][0]["description"]

    print("Weather condition: ", current_weather_condition)

    description_label.text = current_weather_description
    text_area.text = "{:.1f} °C".format(current_temp)

    # Update background image
    set_background(current_weather_condition, tile_grid)

    time.sleep(time_interval)