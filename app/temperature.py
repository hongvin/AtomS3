import busio
import time
import board
import displayio
import terminalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.sparkline import Sparkline
from adafruit_bmp280 import Adafruit_BMP280_I2C

MIN_TEMP = 20
MAX_TEMP = 40

font_file = "fonts/Rubik-Medium-Numeric-31.bdf"
font = bitmap_font.load_font(font_file)

lcd = board.DISPLAY
i2c = busio.I2C(board.D1, board.D2)
bmp280 = Adafruit_BMP280_I2C(i2c,0x76)
bmp280.sea_level_pressure = 1013.25

sensor_label = label.Label(terminalio.FONT, color=0x00ff00, scale=1)
sensor_label.anchor_point = (0.5, 0.0)
sensor_label.anchored_position = (lcd.width//2, 0)
sensor_label.text = "Temperature"

sensor_value = label.Label(font, color=0x00ffff, scale=1)
sensor_value.anchor_point = (0.5, 0.0)
sensor_value.anchored_position = (lcd.width//2, 20)

sparkline = Sparkline(
    width=128,
    height=60,
    max_items=40,
    y_min=MIN_TEMP,
    y_max=MAX_TEMP,
    x=0,
    y=60,
    color=0xFFFFFF,
)

my_group = displayio.Group()
my_group.append(sensor_label)
my_group.append(sensor_value)
my_group.append(sparkline)
lcd.root_group = my_group

while True:
    lcd.auto_refresh = False

    temperature = bmp280.temperature
    sensor_value.text = "{:.1f} °C".format(temperature)
    sparkline.add_value(temperature)
    lcd.auto_refresh = True

    time.sleep(0.5)