import os
import wifi
import time
import socketpool
import ssl
import displayio
import terminalio
import adafruit_requests
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
from adafruit_datetime import datetime
import board
from utils import connect_wifi, display_icon

numeric_font = bitmap_font.load_font("fonts/Rubik-Medium-Numeric-31.bdf")
text_font = bitmap_font.load_font("fonts/LilitaOne-21.bdf")

TARGET="MYR"
BASE="USD"
tz_offset_seconds = 60*60*8
time_interval = 60*5
DATA_SOURCE = (
    "https://api.fxratesapi.com/latest?api_key="
    + os.getenv("FXRATES_KEY") 
    + "&currencies=" + TARGET
    + "&base=" + BASE
)

lcd = board.DISPLAY

print('       Currency  ')
print(' ')
print(' ')
print(' ')

connect_wifi()

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

main_group = displayio.Group()

currency_icon = display_icon("/images/forex/icons8-united-states-64_.bmp", 32, 22)

currency_label = bitmap_label.Label(text_font, color=0x00ff00, scale=1)
currency_label.anchor_point = (0.5, 0.5)
currency_label.anchored_position = (lcd.width // 2, 15)
currency_label.text = f"{BASE}/{TARGET}"

rate_label = bitmap_label.Label(numeric_font,color=0x00ffff, scale=1)
rate_label.anchor_point = (0.5, 0.5)
rate_label.anchored_position = (lcd.width // 2, lcd.height - 35)

last_label = bitmap_label.Label(terminalio.FONT, scale=1)
last_label.anchor_point = (0.5, 0.5)
last_label.anchored_position = (lcd.width // 2, lcd.height - 10)

main_group.append(currency_icon)
main_group.append(currency_label)
main_group.append(rate_label)
main_group.append(last_label)
lcd.root_group = main_group

while True:
    print("Fetching json from", DATA_SOURCE)
    response = requests.get(DATA_SOURCE)
    rates = response.json()["rates"][TARGET]
    timestamp = response.json()["timestamp"]
    timestamp = datetime.fromtimestamp(timestamp+tz_offset_seconds)

    print(f"{BASE}/{TARGET} ({timestamp}): {rates}")

    rate_label.text = "{:.4f}".format(rates)
    last_label.text = "{:0>2d}:{:0>2d}:{:0>2d}".format(timestamp.hour,timestamp.minute,timestamp.second)

    time.sleep(time_interval)