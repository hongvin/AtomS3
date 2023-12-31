import os
import time
import displayio
import wifi
import adafruit_imageload
import busio
import storage
import digitalio
import board

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

def mount_sd(sck,mosi,miso,cs):
    # import sdcardio
    import adafruit_sdcard
    spi = busio.SPI(sck,mosi,miso)
    # sdcard = sdcardio.SDCard(spi, cs)
    cs = digitalio.DigitalInOut(cs)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")

def screenshot(name):
    from adafruit_bitmapsaver import save_pixels
    save_pixels(f'/sd/{name}.bmp')
    print(f"> Screenshot taken, saved into /sd/{name}.bmp")

def mount_screenshot(name,sck=board.D5,mosi=board.D6,miso=board.D7,cs=board.D8):
    try:
        mount_sd(sck,mosi,miso,cs)
        screenshot(name)
        return True
    except Exception as e:
        print('>Error: ',e)
        return False

def display_icon(img,x,y):
    image, palette = adafruit_imageload.load(img,bitmap=displayio.Bitmap,palette=displayio.Palette)
    palette.make_transparent(0)
    tile_grid = displayio.TileGrid(image,pixel_shader = palette)
    tile_grid.x = x
    tile_grid.y = y
    return tile_grid