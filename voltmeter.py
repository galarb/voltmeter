from time import sleep
from ili9341 import Display, color565
import machine
import utime
from xglcd_font import XglcdFont
import sdcard
import os
from bmphandle import read_bmp_file, display_bmp, read_bmp_in_chunks
from voltagecalc import voltage, ang
import math

# SPI and display setup
spi = machine.SPI(1, baudrate=30000000, sck=machine.Pin(18), mosi=machine.Pin(23), miso=machine.Pin(19))
dc = machine.Pin(21)
cs = machine.Pin(5)  # Screen CS
rst = machine.Pin(22)
sd_cs = machine.Pin(2)
display = Display(spi, cs=cs, dc=dc, rst=rst, rotation=90, mirror=False)

# Clear the display
display.clear()

# Load font for displaying text
espresso_dolce = XglcdFont('fonts/EspressoDolce18x24.c', 18, 24)

# Starting point for the line
start_x = 120  # Center of the display horizontally
start_y = 140  # Center of the display vertically
line_length = 80  # Length of the line in pixels

# Initialize SD card (optional, can be removed if not needed)
try:
    sd = sdcard.SDCard(spi, sd_cs)
    os.mount(sd, '/sd')
    print("Files on SD card:", os.listdir('/sd'))
except OSError as e:
    print("Error initializing SD card:", e)

# Previous end coordinates
prev_end_x, prev_end_y = start_x, start_y

read_bmp_in_chunks('/sd/voltmeter1.bmp', display, x_offset=10, y_offset=0)

# Main loop
while True:
    voltage_value = voltage(4)  # Read the voltage from pin 4
    angle = ang(voltage_value)    # Calculate the angle
    radians = math.radians(angle)

    # Calculate the end coordinates of the line
    end_x = int(start_x + line_length * math.cos(radians))
    end_y = int(start_y - line_length * math.sin(radians))  # Invert Y for display coordinates
    # Clear the previous line by drawing it in the background color (black)
    display.draw_line(start_x, start_y, prev_end_x, prev_end_y, color565(255, 255, 255))  # Clear previous line

    # Draw the new line from (start_x, start_y) to (end_x, end_y)
    display.draw_line(start_x, start_y, end_x, end_y, color565(255, 0, 0))  # Draw in red

    # Draw the voltage text
    display.draw_text(40, 240, f'V = {voltage_value:.2f} v', espresso_dolce, color565(255, 0, 0))

    # Update previous end coordinates for the next iteration
    prev_end_x, prev_end_y = end_x, end_y

    # Refresh rate
    sleep(0.01)  # Sleep for 10 ms
