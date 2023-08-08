import os
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

image_path = '20220104_151724.jpg'
reader = easyocr.Reader(['en'])
result = reader.readtext(image_path, paragraph="True")
result
