import os
import wifi
import time
import socketpool
import ssl
import displayio
import terminalio
import adafruit_requests
import adafruit_imageload
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
from utils import connect_wifi, init_display

numeric_font = bitmap_font.load_font("fonts/Rubik-Medium-Numeric-31.bdf")
text_font = bitmap_font.load_font("fonts/LilitaOne-21.bdf")
TARGET="MYR"

display=init_display()

print('       Currency  ')
print(' ')
print(' ')
print(' ')

connect_wifi()

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

DATA_SOURCE = (
    "https://api.fxratesapi.com/latest?api_key="
    + os.getenv("FXRATES_KEY")
)

time_interval = 60*5

image, palette = adafruit_imageload.load("/images/forex/icons8-united-states-64.png")
palette.make_transparent(0)

tile_grid = displayio.TileGrid(image,pixel_shader = palette)
tile_grid.x = display.width // 2 - tile_grid.tile_width // 2
tile_grid.y = display.height // 2 - tile_grid.tile_height // 2

group = displayio.Group()
group.append(tile_grid)

currency_label = bitmap_label.Label(text_font, color=0x00ff00, scale=1)
currency_label.anchor_point = (0.5, 0.5)
currency_label.anchored_position = (display.width // 2, 15)
currency_label.text = f"USD/{TARGET}"

rate_label = bitmap_label.Label(numeric_font,color=0x00ff00, scale=1)
rate_label.anchor_point = (0.5, 0.5)
rate_label.anchored_position = (display.width // 2, display.height - 25)

last_label = bitmap_label.Label(terminalio.FONT, scale=1)
last_label.anchor_point = (0.5, 0.5)
last_label.anchored_position = (display.width // 2, display.height - 25)

main_group = displayio.Group()
main_group.append(group)
main_group.append(currency_label)
main_group.append(rate_label)
display.root_group = main_group

while True:
    print("Fetching json from", DATA_SOURCE)
    response = requests.get(DATA_SOURCE)
    rates = response.json()["rates"][TARGET]
    timestamp = response.json()["timestamp"]

    local_time = datetime.fromtimestamp(timestamp)

    print(f"USD/{TARGET} ({local_time}): {rates}")

    rate_label.text = "{:.2f}".format(rates)

    time.sleep(time_interval)