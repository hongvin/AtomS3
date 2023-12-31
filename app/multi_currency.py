import os
import wifi
import time
import socketpool
import ssl
import displayio
import terminalio
import adafruit_requests
import board
import rtc
import adafruit_ntp
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
from adafruit_datetime import datetime
from utils import connect_wifi

text_font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")

TARGET=["MYR", "CNY", "MYR"]
BASE=["USD","MYR","EUR"]
tz_offset_seconds = 60*60*8
time_interval = 60*5

lcd = board.DISPLAY

print('       Currency  ')
print(' ')
print(' ')
print(' ')

connect_wifi()

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
ntp = adafruit_ntp.NTP(pool, tz_offset=8, server="asia.pool.ntp.org")

connect_wifi()

try: 
    rtc.RTC().datetime = ntp.datetime
except Exception as e:
    print("RTC exception: ", e)
    pass

main_group = displayio.Group()

time_label = bitmap_label.Label(terminalio.FONT,color=0xffff00, scale=1)
time_label.anchor_point = (0.5, 0.5)
time_label.anchored_position = (lcd.width // 2, 0)

last_label = bitmap_label.Label(terminalio.FONT, scale=1)
last_label.anchor_point = (0.5, 0.5)
last_label.anchored_position = (lcd.width // 2, lcd.height - 9)

currency_labels = []
value_labels = []
for i, (target, base) in enumerate(zip(TARGET,BASE)):
    currency_label = bitmap_label.Label(text_font,color=0xffff00, scale=1)
    currency_label.anchor_point = (0.5, 0)
    currency_label.anchored_position = (lcd.width//2, i*38) 
    currency_label.text = f"{base}/{target}"
    currency_labels.append(currency_label)
    main_group.append(currency_label)

    value_label = bitmap_label.Label(terminalio.FONT,color=0x00ff00, scale=2)
    value_label.anchor_point = (0.5, 0)
    value_label.anchored_position = (lcd.width//2, i*38+16)
    value_labels.append(value_label)
    main_group.append(value_label)

main_group.append(time_label)
main_group.append(last_label)
lcd.root_group = main_group

while True:
    for i,(target, base) in enumerate(zip(TARGET,BASE)):
        data_source = f"https://api.fxratesapi.com/latest?api_key={os.getenv("FXRATES_KEY")}&currencies={target}&base={base}"
        print("Fetching json from", data_source)
        response = requests.get(data_source)
        rates = response.json()["rates"][target]
        timestamp = response.json()["timestamp"]
        timestamp = datetime.fromtimestamp(timestamp+tz_offset_seconds)

        print(f"{base}/{target} ({timestamp}): {rates}")

        value_labels[i].text = "{:.4f}".format(rates)
    last_label.text = "Last: {:0>2d}:{:0>2d}:{:0>2d}".format(timestamp.hour,timestamp.minute,timestamp.second)

    time.sleep(time_interval)