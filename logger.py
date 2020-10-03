import datetime
import json
import os
import time
import math

ISO_8601 = '%Y-%m-%d %H:%M:%S.%f'

class Logger:
    def __init__(self, limt=.25):
        self.time_data = {'Daily_limt': limt*60, 'Start_Date_Time': None, 'End_Date_Time':None, 'Time_Spent':0}
        self.emotion_data={'Average_Emotion': None, 'Emotion_Occurrences': []}
    
    def startTimer(self):
        self.time_data['Start_Date_Time'] = str(datetime.datetime.now())
        current_data = {'Time_Data': self.time_data, 'Emotion_Data':self.emotion_data}
        with open(f'productivity_data_{datetime.date.today()}.json', 'w') as f:
            json.dump(current_data, f)
            
    
    def endTimer(self):
        if os.path.exists(f'productivity_data_{datetime.date.today()}.json'):
            with open(f'productivity_data_{datetime.date.today()}.json', 'r+') as f:
                current_data = json.load(f)
                self.time_data['End_Date_Time'] = str(datetime.datetime.now())
                self.update_json()
            
    def updateTimeSpent(self):
        start = datetime.datetime.strptime(self.time_data['Start_Date_Time'], ISO_8601)
        end = datetime.datetime.strptime(self.time_data['End_Date_Time'], ISO_8601)

        self.time_data['Time_Spent'] = math.ceil((end- start).total_seconds())
        with open(f'productivity_data_{datetime.date.today()}.json', 'r+') as f:
                current_data = json.load(f)
                self.time_data['Time_Spent'] = current_data['Time_Data']['Time_Spent'] + self.time_data['Time_Spent']
        self.update_json()
    
    def log_emotion(self, emotion):
        if emotion != '':
            with open(f'productivity_data_{datetime.date.today()}.json') as json_file: 
                self.emotion_data['Emotion_Occurrences'].append((str(datetime.datetime.now()).split()[1].replace(':','-'), emotion))
                self.update_average_emotion()

    def update_average_emotion(self):
        freq = {} 
        for item in self.emotion_data['Emotion_Occurrences']: 
            if (item[1] in freq): 
                freq[item[1]] += 1
            else: 
                freq[item[1]] = 1
        self.emotion_data['Average_Emotion']= (max(freq, key=freq.get))
        self.update_json()

    def update_json(self):
        current_data = {'Time_Data': self.time_data, 'Emotion_Data':self.emotion_data}
        with open(f'productivity_data_{datetime.date.today()}.json', 'r+') as f:
            f.seek(0)
            f.truncate()
            json.dump(current_data, f)
