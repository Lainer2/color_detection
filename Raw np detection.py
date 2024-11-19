import numpy as np

def read_image_raw(file_path):
    
    with open(file_path, 'rb') as f:
        # Read BMP header
        header = f.read(54)
        
        width = int.from_bytes(header[18:22], 'little')
        height = int.from_bytes(header[22:26], 'little')
        
        # Read pixel data
        pixel_data = f.read()
        
        # Calculate row padding (each row must be multiple of 4 bytes)
        row_size = width * 3
        padding = (4 - (row_size % 4)) % 4
        
        # Create numpy array from the pixel data
        image_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Fill the array with pixel values
        for y in range(height):
            for x in range(width):
                pos = y * (row_size + padding) + x * 3
                # BMP stores pixels in BGR order
                image_array[height - 1 - y, x] = [
                    pixel_data[pos + 2],  # R
                    pixel_data[pos + 1],  # G
                    pixel_data[pos]       # B
                ]
                
        return image_array

def save_image_raw(array, file_path):
    
#save np Array as bmp im
    height, width = array.shape[:2]
    
    # Calculate row padding
    row_size = width * 3
    padding = (4 - (row_size % 4)) % 4
    
    # Create file header (14 bytes)
    file_header = bytes([
        0x42, 0x4D,                          # Signature 'BM'
        *(54 + (row_size + padding) * height).to_bytes(4, 'little'),  # File size
        0x00, 0x00, 0x00, 0x00,              # Reserved
        0x36, 0x00, 0x00, 0x00               # Pixel data offset
    ])
    
    # Create info header (40 bytes)
    info_header = bytes([
        0x28, 0x00, 0x00, 0x00,              # Header size
        *width.to_bytes(4, 'little'),         # Width
        *height.to_bytes(4, 'little'),        # Height
        0x01, 0x00,                          # Planes
        0x18, 0x00,                          # Bits per pixel (24)
        0x00, 0x00, 0x00, 0x00,              # Compression (none)
        0x00, 0x00, 0x00, 0x00,              # Image size
        0x00, 0x00, 0x00, 0x00,              # X pixels per meter
        0x00, 0x00, 0x00, 0x00,              # Y pixels per meter
        0x00, 0x00, 0x00, 0x00,              # Colors used
        0x00, 0x00, 0x00, 0x00               # Important colors
    ])
    
    with open(file_path, 'wb') as f:
        f.write(file_header)
        f.write(info_header)
        
        # Write pixel data
        for y in range(height - 1, -1, -1):
            for x in range(width):
                # Write BGR values
                pixel = array[y, x]
                f.write(bytes([pixel[2], pixel[1], pixel[0]]))  # BGR order
            
            # Write padding
            f.write(bytes([0] * padding))
