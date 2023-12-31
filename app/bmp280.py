import busio
import time
import board
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.line import Line
from adafruit_bmp280 import Adafruit_BMP280_I2C
from utils import display_icon

font_file = "fonts/PTSans-NarrowBold-25.bdf"
font = bitmap_font.load_font(font_file)

lcd = board.DISPLAY
i2c = busio.I2C(board.D1, board.D2)
bmp280 = Adafruit_BMP280_I2C(i2c,0x76)
bmp280.sea_level_pressure = 1013.25

main_group = displayio.Group()

top_label = label.Label(font, scale=1, color=0xdddd00)
top_label.anchor_point = (0.5, 0.0)
top_label.anchored_position = (lcd.width//2,0)
top_label.text="BMP280"

top_line = Line(0,25,128,25,0xffffff)

temp_tile = display_icon("/images/bmp280/icons8-temperature-25_.bmp",-2,35)
pressure_tile = display_icon("/images/bmp280/icons8-atmospheric-pressure-25_.bmp",-2,65)
altitude_tile = display_icon("/images/bmp280/icons8-altitude-25_.bmp",-2,95)

temp_label = label.Label(font, scale=1, color=0xd3d3d3)
temp_label.anchor_point = (0.0, 0.0)
temp_label.anchored_position = (25,40)

pressure_label = label.Label(font, scale=1, color=0xd3d3d3)
pressure_label.anchor_point = (0.0, 0.0)
pressure_label.anchored_position = (25,70)

altitude_label = label.Label(font, scale=1, color=0xd3d3d3)
altitude_label.anchor_point = (0.0, 0.0)
altitude_label.anchored_position = (25,100)

main_group.append(top_label)
main_group.append(top_line)
main_group.append(temp_tile)
main_group.append(pressure_tile)
main_group.append(altitude_tile)
main_group.append(temp_label)
main_group.append(pressure_label)
main_group.append(altitude_label)
lcd.root_group = main_group

while True:
    print("\nTemperature: %0.1f C" % bmp280.temperature)
    print("Pressure: %0.1f hPa" % bmp280.pressure)
    print("Altitude = %0.2f meters" % bmp280.altitude)


    temp_label.text = "{:.2f} °C".format(bmp280.temperature)
    pressure_label.text = "{:.1f} hPa".format(bmp280.pressure)
    altitude_label.text = "{:.2f} m".format(bmp280.altitude)
    time.sleep(1)