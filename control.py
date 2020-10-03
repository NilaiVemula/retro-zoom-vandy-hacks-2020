import cv2
import pyvirtualcam
import numpy as np


class Control:
    """ main class for this project. Starts webcam capture and sends output to virtual camera"""

    def __init__(self,  webcam_source=1, width=640, height=480, fps=30):
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

        # print out status
        print('webcam capture started ({}x{} @ {}fps)'.format(self.width, self.height, self.fps))

    def run(self):
        """ contains main while loop to constantly capture webcam, process, and output

        :return: None
        """
        with pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps) as cam:
            # print status
            print('virtual camera started ({}x{} @ {}fps)'.format(cam.width, cam.height, cam.fps))

            while True:
                # STEP 1: capture video from webcam
                ret, raw_frame = self.cam.read()

                # STEP 2: process frames

                # convert frame to RGB
                color_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

                # add alpha channel
                out_frame_rgba = np.zeros((self.height, self.width, 4), np.uint8)
                out_frame_rgba[:, :, :3] = color_frame
                out_frame_rgba[:, :, 3] = 255

                # STEP 3: send to virtual camera
                cam.send(out_frame_rgba)
                cam.sleep_until_next_frame()


# run program
if __name__ == '__main__':
    instance = Control()
    instance.run()