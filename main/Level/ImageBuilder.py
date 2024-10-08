import numpy as np
from PIL import Image


class ImageBuilder:
    def __init__(self, image_path: str = None):
        """
        320x320 image path
        """

        img = Image.open(image_path).convert('L')  # L to grayscale, 1 to black and white
        img = img.resize((320, 320))
        img_array = np.array(img.getdata(), dtype=np.uint8)
        self.img_array = np.reshape(img_array, newshape=(320, 320))
