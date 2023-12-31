import time
import board
import displayio
import terminalio
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.sparkline import Sparkline

MAX_VALUE = 1000

font_file = "fonts/Rubik-Medium-Numeric-31.bdf"
font = bitmap_font.load_font(font_file)

lcd = board.DISPLAY
led_pin = DigitalInOut(board.A5)
led_pin.direction = Direction.OUTPUT
vo_pin = AnalogIn(board.A6)

sensor_label = label.Label(terminalio.FONT, color=0x00ff00, scale=1)
sensor_label.anchor_point = (0.5, 0.0)
sensor_label.anchored_position = (lcd.width//2, 0)
sensor_label.text = "Dust Sensor"

sensor_value = label.Label(font, color=0x00ffff, scale=1)
sensor_value.anchor_point = (0.5, 0.0)
sensor_value.anchored_position = (lcd.width//2, 20)

sparkline = Sparkline(
	width=128,
	height=70,
	max_items=40,
	y_min=0,
	y_max=MAX_VALUE,
	x=0,
	y=58,
	color=0xFFFFFF,
)

my_group = displayio.Group()
my_group.append(sensor_label)
my_group.append(sensor_value)
my_group.append(sparkline)
lcd.root_group = my_group

def read_dust_sensor():
    led_pin.value = False
    time.sleep(0.28)
    vo_raw = vo_pin.value
    led_pin.value = True
    time.sleep(9.62)
    return vo_raw, ((vo_raw /1024)-0.0356)*120*0.035 

while True:
	lcd.auto_refresh = False

	raw_value, dust_value = read_dust_sensor()
	print("Raw: {} | Dust Value: {}".format(raw_value,dust_value))
	sensor_value.text = str(int(dust_value))
	sparkline.add_value(dust_value)
	lcd.auto_refresh = True

	time.sleep(0.1)