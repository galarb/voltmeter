from ili9341 import color565, Display

def read_bmp_in_chunks(filename, display, x_offset=0, y_offset=0, chunk_size=8):
    try:
        with open(filename, 'rb') as f:
            header = f.read(54)  # BMP header is always 54 bytes
            
            # Extract image dimensions and start of pixel data
            width = header[18] + (header[19] << 8)
            height = header[22] + (header[23] << 8)
            pixel_data_start = header[10] + (header[11] << 8)

            # Each row is padded to a multiple of 4 bytes
            row_size = (width * 3 + 3) & ~3

            print(f"Image Width: {width}, Height: {height}, Pixel Data Start: {pixel_data_start}")
            print(f"Row Size (with padding): {row_size}")

            f.seek(pixel_data_start)  # Move to the pixel data start location

            # Read the BMP file in chunks, but flip vertically
            for y in range(0, height, chunk_size):
                lines = []
                # Seek to the bottom of the image and read rows upwards
                for i in range(chunk_size):
                    if y + i < height:
                        row = []
                        # Read a row of pixel data from bottom to top
                        f.seek(pixel_data_start + (height - 1 - (y + i)) * row_size)
                        for x in range(width):
                            b = f.read(1)[0]
                            g = f.read(1)[0]
                            r = f.read(1)[0]
                            row.append(color565(r, g, b))  # Convert RGB to 565 color
                        lines.append(row)

                # Draw the lines starting from the top, after reading chunk
                for i, line in enumerate(lines):
                    display.draw_bitmap_lines(x_offset, y_offset + y + i, line, width)

    except Exception as e:
        print(f"Error reading BMP file: {e}")










def draw_bitmap_line(self, x, y, color_row):
    for i, color in enumerate(color_row):
        self.draw_pixel(x + i, y, color)
        
        
def read_bmp_file(filename):
    with open(filename, 'rb') as f:
        # BMP header is 54 bytes
        header = f.read(54)

        # Get width and height from BMP header
        width = header[18] + (header[19] << 8)
        height = header[22] + (header[23] << 8)

        # Get the starting point of the pixel array
        start = header[10] + (header[11] << 8)

        print(f'Image Width: {width}, Height: {height}, Pixel Data Start: {start}')

        # Seek to the pixel array and read the data
        f.seek(start)
        pixel_data = f.read()

    return width, height, pixel_data

def display_bmp(x, y, width, height, pixel_data):
    # BMP stores pixels as BGR, so you need to convert them to RGB
    for i in range(height):
        for j in range(width):
            b = pixel_data[(i * width + j) * 3]
            g = pixel_data[(i * width + j) * 3 + 1]
            r = pixel_data[(i * width + j) * 3 + 2]
            color = ili9341.color565(r, g, b)
            display.draw_pixel(x + j, y + (height - 1 - i), color)  # Invert the y-axis
