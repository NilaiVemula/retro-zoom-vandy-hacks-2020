# pixle filter

import cv2
import numpy as np

class Filter:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def start(self, raw_frame) :
        # Get input size
        height, width = raw_frame.shape[:2]

        # Desired "pixelated" size
        w, h = (75, 75)

        # Resize input to "pixelated" size
        temp = cv2.resize(raw_frame, (w, h), interpolation=cv2.INTER_LINEAR)

        # re-save pixelated image as raw_frame
        return cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST) 
