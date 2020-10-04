# coinscore class

from PIL import ImageFont, ImageDraw, Image  
import cv2  
import numpy as np  


class CoinScore:
    def __init__(self):
        self.coin_count = 0
        self.coin_img = cv2.imread('assets\coin.png', cv2.IMREAD_UNCHANGED)
        
    
    def overlay_coins(self, frame):
        #cv2.putText(frame, str(self.coin_count), (500, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,0))
        # Pass the image to PIL  
        pil_im = Image.fromarray(frame)  
           
        draw = ImageDraw.Draw(pil_im)  
        # use a truetype font  
        font = ImageFont.truetype("assets\Pixeboy-z8XGD.ttf", 80)  
           
        # Draw the text  
        draw.text((500, 75), str(self.coin_count), font=font)  
           
        # Get back the image to OpenCV  
        frame = cv2.cvtColor(cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2RGB)
        
        self.overlay_image(self.coin_img, frame, (75,550))

        return frame
    
    
    def increment(self):
        self.coin_count += 1

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
