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
        self.state = "stopped"

        # save the screen width and height
        self.screen_width = width
        self.screen_height = height

    def start(self):
        self.state = "running"
        self.coins.clear()

    def end(self):
        self.state = "stopped"
        self.coins.clear()

    def update(self, coin_score, center):
        if self.state == "running":
            if self.bag.contains(center):
                coin_score.coin_count += 1;
                self.bag.goto_random()

                self.create_coins(3, center)
            
            todelete = []
            for i,coin in enumerate(self.coins):
                # apply gravity then move each coin
                coin.yspeed += 0.8
                coin.pos = np.array(coin.pos)
                coin.pos[0] = coin.pos[0] + coin.xspeed 
                coin.pos[1] = coin.pos[1] + coin.yspeed

                # if coin goes below screen, save index to delete
                if coin.pos[1] > self.screen_height:
                    todelete.append(i)
            # delete coins at each index
            for idx in reversed(todelete):
                self.coins.pop(idx)


    def draw(self, frame):
        if self.bag.active:
            self.overlay_image(self.bag.image, frame, (self.bag.pos[1],self.bag.pos[0]))
        
        for coin in self.coins:
            self.overlay_image(coin.image, frame, (coin.pos[1],coin.pos[0]))

    def overlay_image(self, image, frame, offset):
        r,c,b = image.shape

        y1,y2 = offset[0],offset[0] + r
        x1,x2 = offset[1],offset[1] + c

        

        alpha_image = image[:,:,3] / 255.0
        alpha_frame = 1.0-alpha_image

        # if the coins get to the edge of the screen, 
        # they cause errors, so fix that here:
        if alpha_image.shape != image[:,:,0].shape or \
           alpha_frame.shape != frame[y1:y2,x1:x2,0].shape:
           return

        for band in range(0,3):
            frame[y1:y2, x1:x2, band] = (alpha_image * image[:,:,band] + 
                                      alpha_frame * frame[y1:y2, x1:x2, band])

    def create_coins(self,n, center):
        for i in range(5):
            coin = Actor(self.screen_width,self.screen_height, self.coin_img)
            coin.xspeed = random.uniform(-5,5)
            coin.yspeed = random.uniform(-5,-15)
            coin.pos = center
            self.coins.append(coin)
    
   
        
class Actor:
    def __init__(self, width, height, img):
        self.screen_width = width 
        self.screen_height = height
        self.image = img
        self.active = True
        self.pos = np.array([0,0])
        self.height, self.width = self.image.shape[:2]
    
    def goto_random(self):
        self.pos = random.randint(self.width, self.screen_width-self.width), \
                   random.randint(self.height,self.screen_height-self.height)

    def contains(self, point):
        return self.pos[0] < point[0] < self.pos[0] + self.width and \
               self.pos[1] < point[1] < self.pos[1] + self.height

