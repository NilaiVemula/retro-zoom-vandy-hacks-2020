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
                self.data = pd.DataFrame(
                    file_data, columns=['Time', 'Emotion'])

    def create_histogram(self):
        self.type = 'Histogram'
        self.chart = px.histogram(self.data, x='Time', color='Emotion', nbins=20,
                                  barnorm='percent', title='How Your Students are Feeling! - Live Data')
        self.chart.show()

    def create_piechart(self):
        self.type = 'Pie'
        self.chart = px.pie(self.data, names='Emotion',
                            title=f'Students Felt on {datetime.date.today().strftime("%B %d, %Y")}')
        self.chart.show()


if __name__ == "__main__":
    chart1 = Visualization()
    chart1.get_data()
    chart1.create_histogram()
    chart1.create_piechart()

    #chart1.chart.write_html('tmp.html', auto_open=True)
