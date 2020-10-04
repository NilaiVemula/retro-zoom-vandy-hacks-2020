import plotly.express as px
import pandas as pd
import datetime
import os
import json 
class Visualization:
    def __init__(self, chart_type='Bar'):
        self.data = None
        self.visualization = None
        self.type = chart_type
    def get_data(self):
        if os.path.exists(f'productivity_data_{datetime.date.today()}.json'):
                with open(f'productivity_data_{datetime.date.today()}.json', 'r+') as f:
                    file_data = json.load(f)
                    file_data = file_data['Emotion_Data']['Emotion_Occurrences']
                    self.data = pd.DataFrame(file_data, columns=['Time', 'Emotion'])
                    print(self.data)
    def create_visualization(self):
        self.chart = px.histogram(self.data, x='Time', color='Emotion', nbins=20, barnorm='percent')
        #self.chart.show()
if __name__ == "__main__":
    chart1 = Visualization()
    chart1.get_data()
    chart1.create_visualization()

    chart1.chart.write_html('tmp.html', auto_open=True)