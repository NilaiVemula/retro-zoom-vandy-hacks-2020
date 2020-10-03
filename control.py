import cv2
import pyvirtualcam
import numpy as np
import processing
from concurrent.futures import ThreadPoolExecutor
from pynput import keyboard

from CoinGame import CoinGame
from coinscore import CoinScore
from happypipe import HappyPipe


class Control:
    """ main class for this project. Starts webcam capture and sends output to virtual camera"""

    def __init__(self, webcam_source=0, width=640, height=480, fps=30):
        """ sets user preferences for resolution and fps, starts webcam capture

        :param webcam_source: webcam source 0 is the laptop webcam and 1 is the usb webcam
        :type webcam_source: int
        :param width: width of webcam stream
        :type width: int
        :param height: height of webcam stream
        :type height: int
        :param fps: fps of videocam stream
        :type fps: int
        """
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

        # print out status
        print('webcam capture started ({}x{} @ {}fps)'.format(self.width, self.height, self.fps))

        # initialize face attributes
        self.face_position = (0, 0)
        self.face_width = 0
        self.face_height = 0
        self.face_sentiment = ''
        
        # start a thread to call the google cloud api and get the sentiment from the frames
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future_call = self.executor.submit(processing.face_sentiment, None)

        self.key_pressed = ''
        
        # coinGame object
        self.coin_game = CoinGame(self.width,self.height)
        
        # create a coinscore and a happypipe
        self.coin_score = CoinScore()
        self.happy_pipe = HappyPipe()


        # coinGame object
        self.coin_game = CoinGame(self.width,self.height)


    def on_press(self, key):
        try:
            # alphanumeric key
            if key.char == 'c':
                self.key_pressed = 'c'
        except AttributeError:
            # special key
            pass

    def run(self):
        """ contains main while loop to constantly capture webcam, process, and output

        :return: None
        """

        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()  # start to listen for key presses on a separate thread

        with pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps) as virtual_cam:
            # print status
            print(
                'virtual camera started ({}x{} @ {}fps)'.format(virtual_cam.width, virtual_cam.height, virtual_cam.fps))
            virtual_cam.delay = 0
            frame_count = 0
            while True:
                frame_count += 1

                # STEP 1: capture video from webcam
                ret, raw_frame = self.cam.read()
                raw_frame = cv2.flip(raw_frame, 1)

                # STEP 2: process frames
                if raw_frame is None :
                    continue

                # check key presses
                if self.key_pressed == 'c':
                    print('coin game has started')
                    self.key_pressed = ''
                    self.coin_game.start()

                # detect face position
                if frame_count % 3:
                    x,y, self.face_width, self.face_height = processing.face_detection(raw_frame)
                    self.face_position = x,y

                # draw rectangle around face
                cv2.rectangle(raw_frame, self.face_position, (self.face_position[0] + self.face_width,
                                                              self.face_position[1] + self.face_height), (0, 255, 0), 2)

                # check if the api call thread is already running. If not, start it up
                if self.future_call and self.future_call.done():

                    self.face_sentiment = self.future_call.result()
                    self.future_call = self.executor.submit(processing.face_sentiment,raw_frame)
                
                # write sentiment
                cv2.putText(raw_frame, self.face_sentiment, (50, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                            color=(0, 0, 255))
                
                # update pipe status
                self.happy_pipe.update_pipe(self.face_sentiment, self.coin_score)
                # show pipe on screen
                self.happy_pipe.overlay_pipe(raw_frame)
                # show coin score on screen
                self.coin_score.overlay_coins(raw_frame)

                # convert frame to RGB
                color_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

                # add alpha channel
                out_frame_rgba = np.zeros((self.height, self.width, 4), np.uint8)
                out_frame_rgba[:, :, :3] = color_frame
                out_frame_rgba[:, :, 3] = 255

                if self.coin_game.state == 'running':
                    self.coin_game.update((self.face_position[0]+self.face_width//2,
                                           self.face_position[1]+self.face_height//2))
                    self.coin_game.draw(out_frame_rgba)

                # STEP 3: send to virtual camera
                virtual_cam.send(out_frame_rgba)
                virtual_cam.sleep_until_next_frame()


# run program
if __name__ == '__main__':
    instance = Control()
    instance.run()
