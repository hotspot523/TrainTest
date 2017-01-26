from flask import Flask
import pandas as pd
import io
import requests
from flask import render_template

app = Flask(__name__)


@app.route('/')
def train_stats():
    try:
        url = 'http://developer.mbta.com/lib/gtrtfs/Departures.csv'
        df = pd.read_csv(io.StringIO(requests.get(url).content.decode('utf-8')))

        df['ScheduledTime'] = pd.to_datetime(df['ScheduledTime'], unit='s').dt.time
        df['TimeStamp'] = pd.to_datetime(df['TimeStamp'], unit='s').dt.time
        df = df.rename(columns={'TimeStamp': 'Current Time', 'ScheduledTime':'Scheduled Time', 'Lateness': 'Delayed Time (sec)'})
        return render_template('view.html',
                               tables=[df.loc[df.Origin == 'North Station'].replace('NaN','TBD').to_html(classes='north'),
                                       df.loc[df.Origin == 'South Station'].replace('NaN','TBD').to_html(classes='south')],
                               titles = ['na', 'From North', 'From South'])
    except:
        return "Please Wait 10 Seconds and then Refresh: Server is Busy."

if __name__ == '__main__':
    app.run(debug=True, host='localhost',port=5000)
