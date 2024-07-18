import datetime
import requests
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import AndTrigger
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)
dataPCR = {}
baseurl = "https://www.nseindia.com/"
url = f"https://www.nseindia.com/api/option-chain-indices?symbol="
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}

indexes = ["NIFTY", "BANKNIFTY", "FINNIFTY"]
monthName = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
}
gapStrike = {
    "NIFTY": 50,
    "BANKNIFTY": 100,
    "FINNIFTY": 50,
}

def startDataJob():
   sch = BackgroundScheduler(daemon = True)
   now = datetime.datetime.now()
   nseotime = now.replace(hour=9, minute=15)
   nsectime = now.replace(hour=20, minute=30)
   trigger = CronTrigger(start_date=nseotime, end_date=nsectime, day_of_week="mon-fri", minute="*/1")
   sch.add_job(getData, trigger=trigger)
   sch.start()

def getData():
   print("data")
   global dataPCR
   session = requests.Session()
   request = session.get(baseurl, headers=headers, timeout=5)
   cookies = dict(request.cookies)
   for i in indexes:
      response = session.get(url + i, headers=headers, timeout=5, cookies=cookies)
      dataPCR[i] = response.json()

def processData(dt):
   return

@app.route('/')
def index():
   return render_template("index.html")

@app.route('/data')
def data():
   #print(dataPCR)
   return dataPCR

if __name__ == '__main__':
   startDataJob()
   app.run(debug = True)