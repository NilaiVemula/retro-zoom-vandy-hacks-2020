# Get the coins Game

# coin bag appears on screen, you must collect it to make coins rainbow out

import numpy as np
import time
import cv2
import random

class CoinGame:
    

    def __init__(self, width, height):
        # load in and reverse images
        self.coin_img = cv2.imread('assets/coin.png', cv2.IMREAD_UNCHANGED)
        self.coin_img = cv2.cvtColor(self.coin_img, cv2.COLOR_BGRA2RGBA)

        self.coinbag_img = cv2.imread('assets/coinbag.png', cv2.IMREAD_UNCHANGED)
        self.coinbag_img = cv2.cvtColor(self.coinbag_img, cv2.COLOR_BGRA2RGBA)

        # create a bag object
        self.bag = Actor(width, height,self.coinbag_img)
        self.bag.goto_random()

        # create a list for the coins
        self.coins = []

        # create a game state attribute
        self.state = "running"


    def update(self, center):
        if self.state = "running":
            pass
        if self.bag.contains(center):
            print('yee')
            self.bag.goto_random()

    def draw(self, frame):
        if self.bag.active:
            self.overlay_image(self.bag.image, frame, (self.bag.pos[1],self.bag.pos[0]))
            #print(self.bag.pos)

    def overlay_image(self, image, frame, offset):
        r,c,b = image.shape

        y1,y2 = offset[0],offset[0]+image.shape[0]
        x1,x2 = offset[1],offset[1]+image.shape[1]

        alpha_image = image[:,:,3] / 255.0
        alpha_frame = 1.0-alpha_image

        for band in range(0,3):
            frame[y1:y2, x1:x2, band] = (alpha_image * image[:,:,band] + 
                                      alpha_frame * frame[y1:y2, x1:x2, band])

class Actor:
    def __init__(self, width, height, img):
        self.screen_width = width 
        self.screen_height = height
        self.image = img
        self.active = True
        self.pos = np.array([0,0])
        self.height, self.width = self.image.shape[:2]
    
    def goto_random(self):
        self.pos = random.randint(self.width*2, self.screen_width-self.width*2), \
                   random.randint(self.height*2,self.screen_height-self.height*2)

    def contains(self, point):
        return self.pos[0] < point[0] < self.pos[0] + self.width and \
               self.pos[1] < point[1] < self.pos[1] + self.height

