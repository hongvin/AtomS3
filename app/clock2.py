import wifi
import time
import socketpool
import rtc
import gc
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_ntp
from adafruit_bitmap_font import bitmap_font
from utils import connect_wifi, disconnect_wifi

font_file = "fonts/LeagueSpartan-Bold-16.bdf"
font = bitmap_font.load_font(font_file)

lcd = board.DISPLAY

print('         CLOCK  ')
print(' ')
print(' ')
print(' ')

connect_wifi()

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=8, server="asia.pool.ntp.org")

try: 
    rtc.RTC().datetime = ntp.datetime
except Exception as e:
    print("RTC exception: ", e)
    pass
 
time_now = time.localtime()
 
disconnect_wifi()
gc.collect()
 
main_group = displayio.Group()

date_label = label.Label(font,color=0xeb34cc, scale=1)
date_label.anchor_point = (0.5,0.0)
date_label.anchored_position = (lcd.width // 2,0)
date_label.text = "{:0>2d}/{:0>2d}/{}".format(time_now.tm_mday,time_now.tm_mon,time_now.tm_year)

hour_label = label.Label(terminalio.FONT, color=0x00ff00, scale=5)
hour_label.anchor_point = (0.0, 0.0)
hour_label.anchored_position = (0, 20)
hour_label.text = "{:0>2d}".format(time_now.tm_hour)

minute_label = label.Label(terminalio.FONT, color=0x00ffff, scale=5)
minute_label.anchor_point = (0.0, 0.0)
minute_label.anchored_position = (67, 20)
minute_label.text = "{:0>2d}".format(time_now.tm_min)

second_label = label.Label(terminalio.FONT, color=0xffffff, scale=3)
second_label.anchor_point = (0.5, 0.0)
second_label.anchored_position = (lcd.width // 2, 80)
second_label.text = "{:0>2d}".format(time_now.tm_sec)

main_group.append(date_label)
main_group.append(hour_label)
main_group.append(minute_label)
main_group.append(second_label)

lcd.root_group = main_group


while True:
    time_now = time.localtime()
    gc.collect()
    hour_label.text = "{:0>2d}".format(time_now.tm_hour)
    minute_label.text = "{:0>2d}".format(time_now.tm_min)
    second_label.text = "{:0>2d}".format(time_now.tm_sec)
    date_label.text = "{:0>2d}/{:0>2d}/{}".format(time_now.tm_mday,time_now.tm_mon,time_now.tm_year)
            
    time.sleep(0.1)
