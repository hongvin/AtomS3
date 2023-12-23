import os
import time
import displayio
import busio
import board
import wifi
import supervisor
from adafruit_st7789 import ST7789

def connect_wifi():
    if os.getenv("WIFI_SSID")=="":
        print('Please set the wifi \r\ninformation in the \r\nsettings.toml file.')
        print('Exit after 10 seconds')
        time.sleep(1.0)
        for i in range(10):
            time.sleep(1.0)
    else:   
        print(f"Connecting to \r\n[ {os.getenv('WIFI_SSID')} ]")
        while not wifi.radio.connected:
            try:
                wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASS"))
            except Exception as ex:
                print(ex)
            time.sleep(0.1)
            print('.')
        print(f"Connected to {os.getenv('WIFI_SSID')}")
        print(f"My IP address: {wifi.radio.ipv4_address}")

def disconnect_wifi():
    wifi.radio.stop_station()
    wifi.radio.enabled=False
    
def init_display():
    displayio.release_displays()
    spi = busio.SPI(board.LCD_CLK,board.LCD_MOSI)
    while not spi.try_lock():
        pass
    spi.configure(baudrate=24000000) # Configure SPI for 24MHz
    spi.unlock()
    display_bus = displayio.FourWire(spi,command=board.LCD_DC,chip_select=board.LCD_CS) 
    display = ST7789(display_bus, width=128, height=128, colstart=2,rowstart=1)

    TERMINAL_HEIGHT=display.height+20
    display.root_group.scale = 1
        
    display.root_group[0].hidden = False
    display.root_group[1].hidden = True # logo
    display.root_group[2].hidden = True # status bar
    supervisor.reset_terminal(display.width,TERMINAL_HEIGHT)
    display.root_group[0].y = 0

    return display
