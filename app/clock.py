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

hour_label = label.Label(terminalio.FONT, color=0x00ff00, scale=6)
hour_label.anchor_point = (1.0, 0.0)
hour_label.anchored_position = (lcd.width-1, -8)
hour_label.text = "{:0>2d}".format(time_now.tm_hour)

minute_label = label.Label(terminalio.FONT, color=0x00ffff, scale=6)
minute_label.anchor_point = (1.0, 0.0)
minute_label.anchored_position = (lcd.width-1, 47)
minute_label.text = "{:0>2d}".format(time_now.tm_min)

date_label = label.Label(font,color=0xeb34cc, scale=1)
date_label.anchor_point = (1.0,0.0)
date_label.anchored_position = (lcd.width-10, 110)
date_label.text = "{:0>2d}/{:0>2d}".format(time_now.tm_mday,time_now.tm_mon)

main_group.append(hour_label)
main_group.append(minute_label)
main_group.append(date_label)

WEEK_COLOR_NOW = 0xCCCCCC
WEEK_COLOR_NOTNOW=0x444444
week_id = time_now.tm_wday
week_label=[]
weeks = ("MON","TUE","WED","THU","FRI","SAT","SUN")
for i in range(7):
    wlabel = label.Label(font, color=WEEK_COLOR_NOTNOW, scale=1)
    wlabel.anchor_point = (0.0, 0.0)
    wlabel.anchored_position = (0, i*19)
    wlabel.text = f"{weeks[i]}"
    week_label.append(wlabel)
    main_group.append(wlabel)
    
week_label[week_id].color = WEEK_COLOR_NOW

lcd.root_group = main_group

while True:
    time_now = time.localtime()
    gc.collect()
    hour_label.text = "{:0>2d}".format(time_now.tm_hour)
    minute_label.text = "{:0>2d}".format( time_now.tm_min)
    
    if time_now.tm_wday != week_id:
        week_label[week_id].color = WEEK_COLOR_NOTNOW
        week_label[time_now.tm_wday].color = WEEK_COLOR_NOW
        weekid = time_now.tm_wday
    
    date_label.text = "{:0>2d}/{:0>2d}".format(time_now.tm_mday,time_now.tm_mon)
            
    time.sleep(1)
