import sys
import fileinput
import base64
import numpy as np
import cv2
from PIL import Image
import io

try:
    base64image = ""
    for line in fileinput.input():
        base64image += line
    if len(base64image) % 4:
    # not a multiple of 4, add padding:
        base64image += '=' * (4 - len(base64image) % 4)
    header, data = base64image.split(',', 1)
    decoded_image = base64.b64decode(data)
    nparr = np.frombuffer(decoded_image, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    # Process input
    sys.stdout.write("decoded image successfully")
    sys.stdout.flush()

except(err):
    print(err)