import busio
import time
import board
import displayio
import terminalio
from analogio import AnalogIn
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.sparkline import Sparkline

MAX_VALUE = 255

font_file = "fonts/Rubik-Medium-Numeric-31.bdf"
font = bitmap_font.load_font(font_file)

lcd = board.DISPLAY
analog_in = AnalogIn(board.A1)

sensor_label = label.Label(terminalio.FONT, color=0x00ff00, scale=1)
sensor_label.anchor_point = (0.5, 0.0)
sensor_label.anchored_position = (lcd.width//2, 0)
sensor_label.text = "Analog Read"

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

while True:
	lcd.auto_refresh = False

	analog_value = int(analog_in.value/65535*MAX_VALUE)
	sensor_value.text = str(analog_value)
	sparkline.add_value(analog_value)
	lcd.auto_refresh = True

	time.sleep(0.1)