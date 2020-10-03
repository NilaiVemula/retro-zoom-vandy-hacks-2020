# Get the coins Game

# coin bag appears on screen, you must collect it to make coins rainbow out

import numpy as np
import time
import cv2

class CoinGame:
    

    def __init__(self):
        self.coin_img = cv2.imread('assets/coin.png', cv2.IMREAD_UNCHANGED)
        cv2.cvtColor(self.coin_img,cv2.COLOR_BGR2RGB)

    def update(self, pos):
        pass 

    def draw(self, frame):
        print(self.coin_img.shape)
        r,c,b = self.coin_img.shape

        

        frame[100:100+r, 100:100+c,:] = self.coin_img
        