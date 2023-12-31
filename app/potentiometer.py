import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from analogio import AnalogIn
from gauge_utils import Gauge

lcd = board.DISPLAY
potentiometer = AnalogIn(board.A5)

print('   Potentiometer  ')
print(' ')
print(' ')
print(' ')

main_group = displayio.Group()

sensor_label = label.Label(terminalio.FONT, color=0x00ff00, scale=1)
sensor_label.anchor_point = (0.5, 0.0)
sensor_label.anchored_position = (lcd.width//2, 0)
sensor_label.text = "Potentiometer"

gauge = Gauge(0,65536, 128, 105,display_value=False)

sensor_value = label.Label(terminalio.FONT, color=0x00ffff, scale=2)
sensor_value.anchor_point = (0.5, 0.0)
sensor_value.anchored_position = (lcd.width//2, 105)

main_group.append(sensor_label)
main_group.append(gauge)
main_group.append(sensor_value)
lcd.root_group = main_group

while True:
    sensor_value.text=str(potentiometer.value)
    gauge.update(potentiometer.value)
    time.sleep(0.5)