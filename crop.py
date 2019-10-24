from cv2 import cv2
# import numpy as np
import matplotlib.pyplot as plt

def crop(imagePath, coords, saveLocation):
    img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    x1 = coords["x1"]
    x2 = coords["x2"]
    y1 = coords["y1"]
    y2 = coords["y2"]
    croppedImage = img[y1:y2, x1:x2]
    cv2.imwrite(saveLocation, croppedImage)

if __name__ == "__main__":
    image = "ran.jpg"
    cropSize = {"x1": 1200, "y1": 400,"x2": 2700,"y2": 2400 }
    imagePath = "cropped_images//"
    imageName = 'ran_cropped'
    for i in range(2):
        crop(image, cropSize, imagePath + imageName + ".jpg")
        delta = cropSize["x2"] - cropSize["x1"]
        cropSize["x1"] += delta + 150
        cropSize["x2"] += delta + 150
        imageName += "2"
