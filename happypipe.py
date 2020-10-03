# happinesspipe 
import cv2

class HappyPipe:

    def __init__(self):
        self.pipe_image = cv2.imread('assets\pipeline.png', cv2.IMREAD_UNCHANGED)
        self.progress_count = 0




    def overlay_pipe(self,frame):
        if self.progress_count < 1:
            return
        pipe_image = cv2.resize(self.pipe_image, (int(self.progress_count),100), interpolation = cv2.INTER_AREA)
        self.overlay_image(pipe_image, frame, (50,50))

    def update_pipe(self,sentiment, coin_score):
        if sentiment == 'joy':
            self.progress_count +=1
        elif sentiment == 'angry' and self.progress_count > 1:
            self.progress_count -= 1
        if self.progress_count >= 250:
            self.progress_count = 1
            coin_score.increment()

    
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