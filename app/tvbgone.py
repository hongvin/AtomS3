import array
import time
import board
import pulseio
import displayio
import terminalio
from adafruit_display_text import bitmap_label
from utils import display_icon

lcd = board.DISPLAY

print('      TVBGone  ')
print(' ')
print(' ')
print(' ')

main_group = displayio.Group()

tvb_icon = display_icon("/images/tvbgone/icon.bmp", 14, 25)

tvb_label = bitmap_label.Label(terminalio.FONT, color=0x00ff00, scale=2)
tvb_label.anchor_point = (0.5, 0)
tvb_label.anchored_position = (lcd.width // 2, 0)
tvb_label.text="TV B Gone"

frequency_label = bitmap_label.Label(terminalio.FONT, scale=1)
frequency_label.anchor_point = (0.5, 0.5)
frequency_label.anchored_position = (lcd.width // 2, 110)

main_group.append(tvb_icon)
main_group.append(tvb_label)
main_group.append(frequency_label)
lcd.root_group = main_group

while True:
    time.sleep(0.5)  # Give a half second before starting

    f = open("/files/tvbgone.txt", "r")
    for line in f:
        code = eval(line)
        print(code)

        try:
            repeat = code["repeat"]
            delay = code["repeat_delay"]
        except KeyError:  
            delay = 0

        table = code["table"]
        pulses = []  
        
        for i in code["index"]:
            pulses += table[i]
        pulses.pop() 
        frequency_label.text = f"Freq: {code["freq"]}"

        with pulseio.PulseOut(
            board.IR_LED, frequency=code["freq"], duty_cycle=2**15
        ) as pulse:
            for i in range(repeat):
                try:
                    pulse.send(array.array("H", pulses))
                    time.sleep(delay)
                except:
                    continue

        time.sleep(code["delay"])

    f.close()