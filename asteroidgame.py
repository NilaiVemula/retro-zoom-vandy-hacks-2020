# asteroid game 

import cv2
import random
import numpy as np

class AsteroidGame:

    def __init__(self, width, height):
        self.asteroid_image = cv2.imread('assets/asteroid.png', cv2.IMREAD_UNCHANGED)
        self.asteroid_image = cv2.cvtColor(self.asteroid_image, cv2.COLOR_BGRA2RGBA)

        self.asteroids = []

        self.width = width
        self.height = height 

        self.count = 0
    
    def start(self):
        pass

    def end(self):
        self.asteroids.clear()

    def update(self, face):
        self.count += 1
        if self.count % 15 == 0:
            ast = Actor(self.width,self.height, self.asteroid_image)
            x = random.randint(0,self.width)
            y = 0
            ast.pos = np.array([x,y])

            ast.xspeed = random.randint(-5,5)
            ast.yspeed = random.randint(3,15)
            self.asteroids.append(ast)
        
        for ast in self.asteroids:
            ast.pos = np.array(ast.pos)
            ast.pos[0] += ast.xspeed 
            ast.pos[1] += ast.yspeed
    
    def draw(self,frame):
        for ast in self.asteroids:
            self.overlay_image(ast.image, frame, (ast.pos[1],ast.pos[0]))
        
    
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

    def contains(self, point):
        return self.pos[0] < point[0] < self.pos[0] + self.width and \
               self.pos[1] < point[1] < self.pos[1] + self.height

    def collide_rect(self,rect):
        pass