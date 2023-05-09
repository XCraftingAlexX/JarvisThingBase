import cv2
import numpy as np
import os
from PIL import Image

# Create the references directory if it doesn't exist
if not os.path.exists("references"):
    os.mkdir("references")

# Load the new image
new_img_path = "path/to/new/image.jpg"
new_img = cv2.imread(new_img_path)

# Convert the image to an Image object
new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
img = Image.fromarray(new_img)

# Make the background transparent
img = img.convert("RGBA")
datas = img.getdata()
newData = []
for item in datas:
    if item[0] < 200 and item[1] < 200 and item[2] < 200:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)
img.putdata(newData)

# Save the image to the references folder with a unique filename
filename = f"reference_{time.time()}.png"
img.save(os.path.join("references", filename), "PNG")