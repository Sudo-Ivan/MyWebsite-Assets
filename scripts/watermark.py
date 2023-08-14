import os
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def add_watermark(directory, watermark_path, position, margin):
    _, watermark_extension = os.path.splitext(watermark_path)
    
    if watermark_extension == ".svg":
        watermark = svg2rlg(watermark_path)
    elif watermark_extension == ".png":
        watermark = Image.open(watermark_path).convert("RGBA")
    else:
        raise ValueError("Invalid watermark file format. Please use either SVG or PNG.")

    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(directory, filename)
            image = Image.open(image_path)

            width, height = image.size
            watermark_width = width // 5
            watermark_height = watermark_width * watermark.height // watermark.width
            watermark_resized = watermark.resize((watermark_width, watermark_height))

            if position == "bottom-left":
                watermark_x = margin
                watermark_y = height - watermark_resized.height - margin
            elif position == "bottom-right":
                watermark_x = width - watermark_resized.width - margin
                watermark_y = height - watermark_resized.height - margin
            else:
                raise ValueError("Invalid position argument. Please use 'bottom-left' or 'bottom-right'.")

            image.paste(watermark_resized, (watermark_x, watermark_y), watermark_resized)
            image.save(os.path.join(directory, f"watermarked_{filename}"))

            print(f"Watermark added to {filename}")

# Example usage
directory_path = "wallpapers"
watermark_path = "watermark.png"
position = input("Enter the watermark position (bottom-left / bottom-right) [default: bottom-right]: ") or "bottom-right"
margin = int(input("Enter the margin or spacing value for the watermark [default: 10]: ") or 10)

try:
    add_watermark(directory_path, watermark_path, position, margin)
except Exception as e:
    print(f"An error occurred: {e}")