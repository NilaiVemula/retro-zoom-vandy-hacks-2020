from PIL import ImageGrab
import win32gui

from sentiment import face_sentiment

import numpy as np




class GroupSentiment:
    def __init__(self):
        self.window = ''
        self.toplist, self.winlist = [], []

    def enum_cb(self, hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


    def take_screenshot(self):



        win32gui.EnumWindows(self.enum_cb, self.toplist)

        zoom = [(hwnd, title) for hwnd, title in self.winlist if 'Zoom Meeting' in title]
        # just grab the hwnd for first window matching firefox
        if not zoom:
            print('Zoom Meeting not found')
            return None
        zoom = zoom[0]
        hwnd = zoom[0]

        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)
        img = np.array(img)
        return img

    def run(self):
        print('Starting')

        while True:
            screenshot = self.take_screenshot()
            if screenshot is not None:
                emotions = face_sentiment(screenshot)
                print(emotions)
            else:
                print('fuck')



if __name__ == '__main__':
    a = GroupSentiment()
    a.run()
