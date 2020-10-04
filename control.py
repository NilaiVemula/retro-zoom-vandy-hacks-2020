import cv2
import pyvirtualcam
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import processing
from concurrent.futures import ThreadPoolExecutor
from pynput import keyboard

from CoinGame import CoinGame
from coinscore import CoinScore
from happypipe import HappyPipe
from asteroidgame import AsteroidGame
from video_filter import Filter


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

        # start a thread to call the google cloud api and get the object from the frames
        self.future_call_1 = self.executor.submit(processing.localize_objects, None)
        
        # list of objects detected in the frame
        self.objects = []
        # list of objects in the scavenger hunt that need to be found
        self.need_to_find = ['Person', 'Glasses']
        self.scavenger = False

        self.key_pressed = ''
        self.game = None
        
        # create a coinscore and a happypipe
        self.coin_score = CoinScore()
        self.happy_pipe = HappyPipe()

        # coinGame object
        self.coin_game = CoinGame(self.width,self.height)

        # asteroid game object
        self.asteroid_game = AsteroidGame(self.width, self.height)

        # filter object
        self.videofilter = Filter(self.width, self.height)


    def on_press(self, key):
        try:
            # alphanumeric key
            self.key_pressed = str(key.char)
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

                # map keys to games:
                keymap = {'c':self.coin_game,'a':self.asteroid_game}
                # check if key pressed corresponds to a game
                if self.key_pressed in keymap:
                    # end the old game
                    if self.game:
                        self.game.end()
                    self.scavenger = False
                    # if the new game is different, then start the new game
                    if keymap[self.key_pressed] != self.game:
                        keymap[self.key_pressed].start()
                        self.game = keymap[self.key_pressed]
                    else:
                        self.game = None
                    
                    # reset the key pressed
                    self.key_pressed = ''
                # retro filter
                if self.key_pressed == 'f':
                    raw_frame = self.videofilter.start(raw_frame)
                    self.key_pressed = ''
                # scavenger hunt game
                if self.key_pressed == 's': 
                    self.key_pressed = ''
                    
                    self.scavenger = not self.scavenger
                    if self.game:
                        self.game.end()
                        self.game = None
                    self.need_to_find = ['Person', 'Glasses']



                # detect face position
                if frame_count % 3:
                    x,y, self.face_width, self.face_height = processing.face_detection(raw_frame)
                    self.face_position = x,y

                # draw rectangle around face
                # cv2.rectangle(raw_frame, self.face_position, (self.face_position[0] + self.face_width,
                #                                               self.face_position[1] + self.face_height), (0, 255, 0), 2)

                # Face Sentiment: check if the api call thread is already running. If not, start it up
                if self.future_call and self.future_call.done():

                    self.face_sentiment = self.future_call.result()
                    self.future_call = self.executor.submit(processing.face_sentiment,raw_frame)

                # Object detection: check if the api call thread is already running. If not, start it up
                # only do this if the scav hunt game is running
                if self.scavenger and self.future_call_1 and self.future_call_1.done():
                    self.objects = self.future_call_1.result()
                    self.future_call_1 = self.executor.submit(processing.localize_objects, raw_frame)
                    
                    
                    # remove found objects from the need to find list
                    found_objects = list(set(self.objects) & set(self.need_to_find))
                    for object in found_objects:
                        self.need_to_find.remove(object)


                # write sentiment
                # cv2.putText(raw_frame, self.face_sentiment, (50, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                #             color=(0, 0, 255))
                
                # update pipe status
                self.happy_pipe.update_pipe(self.face_sentiment, self.coin_score)
                # show pipe on screen
                self.happy_pipe.overlay_pipe(raw_frame)
                # show coin score on screen
                raw_frame = self.coin_score.overlay_coins(raw_frame)

                # display need to find objects
                if self.scavenger:
                    pil_im = Image.fromarray(raw_frame)
                    
                    draw = ImageDraw.Draw(pil_im)

                    font = ImageFont.truetype("assets\Pixeboy-z8XGD.ttf", 50)
                    
                    # draw the text
                    if len(self.need_to_find) > 0:
                        # print(self.need_to_find)
                        draw.text((50,65), "Show Me:",font=font)
                        for i in range(len(self.need_to_find)):
                            draw.text((50,115+50*i), self.need_to_find[i], font=font)
                    else:
                        draw.text((50,65), "I am Satisfied", font=font)
                    
                    raw_frame = cv2.cvtColor(cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2RGB)
        
                # convert frame to RGB
                color_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

                # add alpha channel
                out_frame_rgba = np.zeros((self.height, self.width, 4), np.uint8)
                out_frame_rgba[:, :, :3] = color_frame
                out_frame_rgba[:, :, 3] = 255

                if self.game == self.coin_game:
                    self.coin_game.update(self.coin_score,
                                          (self.face_position[0]+self.face_width//2,
                                           self.face_position[1]+self.face_height//2))
                    self.coin_game.draw(out_frame_rgba)

                if self.game == self.asteroid_game:

                    self.asteroid_game.update((self.face_position[0], self.face_width, \
                                               self.face_position[1], self.face_height), raw_frame)
                    out_frame_rgba = self.asteroid_game.draw(out_frame_rgba)

                
                # STEP 3: send to virtual camera
                virtual_cam.send(out_frame_rgba)
                virtual_cam.sleep_until_next_frame()


# run program
if __name__ == '__main__':
    instance = Control()
    instance.run()
