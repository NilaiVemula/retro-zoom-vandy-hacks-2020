from PIL import ImageGrab
import win32gui

from sentiment import face_sentiment

import numpy as np

import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import sys


class GroupSentiment(tk.Frame):
    def __init__(self, master=None):
        self.toplist, self.winlist = [], []
        tk.Frame.__init__(self,master)
        self.createWidgets()


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

    def createWidgets(self):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111)


        # bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=0, column=1)
        canvas.draw()

        self.plotbutton = tk.Button(master=root, text="plot", command=lambda: self.plot(canvas, ax))
        self.plotbutton.grid(row=0, column=0)

        while True:
            self.plot(canvas, ax)

    def plot(self, canvas, ax):
        print('Starting')

        screenshot = self.take_screenshot()
        if screenshot is not None:
            emotions = face_sentiment(screenshot)
            print(emotions)

            data = {'Emotions': ['anger', 'joy', 'surprise', 'sorrow'],
                     'Values': emotions
                     }
            df = pd.DataFrame(data, columns=['Emotions', 'Values'])
            df = df[['Emotions', 'Values']].groupby('Emotions').sum()
            df.plot(kind='bar', legend=True, ax=ax)
            ax.set_title('Group Sentiment')
            canvas.draw()
            ax.clear()
        else:
            print('ERROR')



if __name__ == '__main__':
    root = tk.Tk()
    app = GroupSentiment(master=root)
    app.mainloop()
