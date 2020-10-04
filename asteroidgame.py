# asteroid game 

import cv2
import random
import numpy as np
import pathlib

from playsound import playsound

class AsteroidGame:

    def __init__(self, width, height):
        self.asteroid_image = cv2.imread('assets/asteroid.png', cv2.IMREAD_UNCHANGED)
        self.asteroid_image = cv2.cvtColor(self.asteroid_image, cv2.COLOR_BGRA2RGBA)

        self.heart_image = cv2.imread('assets/heart.png', cv2.IMREAD_UNCHANGED)
        self.heart_image = cv2.cvtColor(self.heart_image, cv2.COLOR_BGRA2RGBA)

        self.heart_broken_image = cv2.imread('assets/heart_broken.png', cv2.IMREAD_UNCHANGED)
        self.heart_broken_image = cv2.cvtColor(self.heart_broken_image, cv2.COLOR_BGRA2RGBA)

        self.explosion_image = cv2.imread('assets/explosion.png', cv2.IMREAD_UNCHANGED)
        self.explosion_image = cv2.cvtColor(self.explosion_image, cv2.COLOR_BGRA2RGBA)

        self.sound_path = str(pathlib.Path(__file__).parent.absolute()/'assets/damage.wav')

        self.asteroids = []

        self.screen_width = width
        self.screen_height = height 

        self.count = 0

        self.hearts = []
        for i in range(3):
            heart = Actor(width, height, self.heart_image)
            heart.pos = (i*70+20, height-120)
            self.hearts.append(heart)
        self.heart_index = 2

        self.state = "start"
        

    
    def start(self):
        self.hearts = []
        for i in range(3):
            heart = Actor(self.screen_width, self.screen_height, self.heart_image)
            heart.pos = (i*70+20, self.screen_height-120)
            self.hearts.append(heart)
        self.heart_index = 2

    def end(self):
        self.asteroids.clear()
        self.state = "end"

    def update(self, center):
        self.count += 1
        if self.count % 15 == 0 and self.heart_index >= 0:
            ast = Actor(self.screen_width,self.screen_height, self.asteroid_image)
            x = random.randint(0,self.screen_width)
            y = 0
            ast.pos = np.array([x,y])

            ast.xspeed = random.randint(-5,5)
            ast.yspeed = random.randint(3,10)
            self.asteroids.append(ast)
        
        # move each asteroid and check if it collides with face
        toremove = []
        for i,ast in enumerate(self.asteroids):
            ast.pos = np.array(ast.pos)
            ast.pos[0] += ast.xspeed 
            ast.pos[1] += ast.yspeed
            if ast.contains((ast.pos[0],ast.pos[1],ast.image.shape[1],ast.image.shape[0]), center) and self.heart_index >= 0:
                print("hit!")
                playsound(self.sound_path)
                self.hearts[self.heart_index].image = self.heart_broken_image
                self.heart_index -= 1
                toremove.append(i) 
        for idx in sorted(toremove, reverse=True):
            print(idx)
            self.asteroids.pop(idx)
        
        # remove any asteroids that go below the screen
        toremove = []
        for i,ast in enumerate(self.asteroids):
            if ast.pos[1] > self.screen_height:
                toremove.append(i)
        for idx in sorted(toremove, reverse=True):
            self.asteroids.pop(idx)
        
        print(len(self.asteroids))
    
    def draw(self,frame):
        for ast in self.asteroids:
            self.overlay_image(ast.image, frame, (ast.pos[1],ast.pos[0]))
        
        for h in self.hearts:
            self.overlay_image(h.image, frame, (h.pos[1],h.pos[0]))
        
    
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

    def contains(self, rect, point):
        pos = rect[:2]
        width,height = rect[2:]
        return pos[0] < point[0] < pos[0] + width and \
               pos[1] < point[1] < pos[1] + height
