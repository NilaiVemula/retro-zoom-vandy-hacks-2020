import cv2
import pyvirtualcam
import numpy as np
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vandy-hacks-2020-a026305d4125.json'

from processing import face_detection, get_emotion

from concurrent.futures import ThreadPoolExecutor

class Control:
    """ main class for this project. Starts webcam capture and sends output to virtual camera"""

    def __init__(self,  webcam_source=0, width=640, height=480, fps=30):
        """ sets user preferences for resolution and fps, starts webcam capture

        :param webcam_source:
        :type webcam_source: int
        :param width:
        :type width: int
        :param height:
        :type height: int
        :param fps:
        :type fps: int
        """
        # constructor for the control class
        # on my computer, webcam source 0 is the laptop webcam and 1 is the usb webcam
        self.webcam_source = webcam_source

        # initialize webcam capture
        self.cam = cv2.VideoCapture(self.webcam_source)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cam.set(cv2.CAP_PROP_FPS, fps)

        # Query final capture device values (different from what i set??)
        # save as object variables
        self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)
        
        # store the emotions
        self.emotions = None

        # start a thread to call the google cloud api and get the sentiment from the frames
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future_call = self.executor.submit(get_emotion,None)
        

        

        # print out status
        print('webcam capture started ({}x{} @ {}fps)'.format(self.width, self.height, self.fps))

    def run(self):
        """ contains main while loop to constantly capture webcam, process, and output

        :return: None
        """
        with pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps) as virtual_cam:
            # print status
            print('virtual camera started ({}x{} @ {}fps)'.format(virtual_cam.width, virtual_cam.height, virtual_cam.fps))
            virtual_cam.delay = 0
            frame_count = 0
            while True:
                frame_count += 1

                # STEP 1: capture video from webcam
                ret, raw_frame = self.cam.read()

                # check if the api call thread is already running. If not, start it up
                if self.future_call and self.future_call.done():

                    self.emotions = self.future_call.result()
                    self.future_call = self.executor.submit(get_emotion,raw_frame)
                    print("completed")


                # STEP 2: detect any faces in the frame
                self.faces = face_detection(raw_frame)

                # draw rectangles around faces
                for (x,y,w,h) in self.faces:
                    cv2.rectangle(raw_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                if self.emotions: 
                    print(self.emotions)
                    # there is an emotion to work with
                
                # if frame_count == 60:
                #     raw_frame, face_position = processing.face_detection(raw_frame)

                #     if 200< face_position[0] < 400 and 100< face_position[1] < 300:
                #         print('Yay')

                #     frame_count = 0

                # talk to google emotion api

                

                # convert frame to RGB
                color_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

                # add alpha channel
                out_frame_rgba = np.zeros((self.height, self.width, 4), np.uint8)
                out_frame_rgba[:, :, :3] = color_frame
                out_frame_rgba[:, :, 3] = 255

                # STEP 3: send to virtual camera
                virtual_cam.send(out_frame_rgba)
                virtual_cam.sleep_until_next_frame()
    
    def __exit__(self, exec_type, exc_value, traceback):
        self.cam.release()
        self.api_thread.join()
        self.executor.shutdown()
        print('successfully freed resources')


# run program
if __name__ == '__main__':
    instance = Control()
    instance.run()
    
