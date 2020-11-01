import requests
import json
import urllib.parse
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.blocking import BlockingScheduler


def get_token(user, password):
    url = 'https://api.ecoledirecte.com/v3/login.awp'
    prepayload = {"identifiant": user, "motdepasse": password}
    payload = {'data': f'{json.dumps(prepayload)}'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'api.ecoledirecte.com',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br',
               'Origin': 'https://www.ecoledirecte.com', 'DNT': '1', 'Connection': 'keep-alive',
               'Refer': 'https://www.ecoledirecte.com/'}
    r = requests.post(url, data=payload, headers=headers)
    json_str = json.dumps(r.json())
    resp = json.loads(json_str)
    global id
    id = resp['data']['accounts'][0]['id']
    return resp['token']


def get_id(user, password):
    url = 'https://api.ecoledirecte.com/v3/login.awp'
    prepayload = {"identifiant": user, "motdepasse": password}
    payload = {'data': f'{json.dumps(prepayload)}'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'api.ecoledirecte.com',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br',
               'Origin': 'https://www.ecoledirecte.com', 'DNT': '1', 'Connection': 'keep-alive',
               'Refer': 'https://www.ecoledirecte.com/'}
    r = requests.post(url, data=payload, headers=headers)
    json_str = json.dumps(r.json())
    resp = json.loads(json_str)
    return resp['data']['accounts'][0]['id']


def get_timeline():
    url = f'https://api.ecoledirecte.com/v3/E/{get_id(user, password)}/emploidutemps.awp?verbe=get'
    prepayload = {"dateDebut": startDate, "dateFin": endDate, "avecTrous": "false",
                  "token": get_token(user, password)}
    payload = {'data': f'{json.dumps(prepayload)}'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'api.ecoledirecte.com',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br',
               'Origin': 'https://www.ecoledirecte.com', 'DNT': '1', 'Connection': 'keep-alive',
               'Refer': f'https://www.ecoledirecte.com/Eleves/{get_id(user, password)}/EmploiDuTemps'}

    r = requests.post(url, data=payload, headers=headers, params={'verbe': 'get'})
    json_str = json.dumps(r.json())
    resp = json.loads(json_str)
    return resp['data']


def correct_time(date):
    date = datetime.strptime(date, '%Y-%m-%d %H:%M') - timedelta(hours=1, minutes=0)
    date = date.strftime("%Y%m%dT%H%M00")
    return date


def timeline_final():
    timeline = get_timeline()
    for item in timeline:
        item['end_date'] = item['end_date'].replace('24:00', '23:00')
    for i in range(len(timeline)):
        timeline[i]['start_date'] = correct_time(timeline[i]['start_date'])
    for i in range(len(timeline)):
        timeline[i]['end_date'] = correct_time(timeline[i]['end_date'])
    return timeline


def timeline_to_ical():
    ical = {"name": "calendar.ical", "data": timeline_final(), "version": "4.3.0"}
    ical = urllib.parse.quote(json.dumps(ical))
    ical = "data=" + ical + "&type=ical"
    url = 'https://export.dhtmlx.com/scheduler'
    payload = ical
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'export.dhtmlx.com',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate, br',
               'Origin': 'https://www.ecoledirecte.com', 'DNT': '1', 'Connection': 'keep-alive',
               'Refer': 'https://www.ecoledirecte.com/Eleves/7966/EmploiDuTemps'}
    r = requests.post(url, data=payload, headers=headers)
    os.chdir(r"/calendar")
    open('calendar.ical', 'wb').write(r.content)
    print(datetime.now())


user = os.environ['MY_USER']
password = os.environ['MY_PASS']
startDate = os.environ['startDate']
endDate = os.environ['endDate']

timeline_to_ical()

scheduler = BlockingScheduler()
job = scheduler.add_job(timeline_to_ical, 'interval', minutes=45)
scheduler.start()
