# Configuration Variables

# ArcGIS Monitor:
monitorSite='https://mymonitor.domain.local'
username="dashboard"

# ArcGIS Feature Services
featureServiceID="itemid"

# Constant variables
system="ArcGIS_Monitor"
profileName = "dashboard"

# imports
import keyring
import requests
import datetime
from arcgis.gis import GIS

# main
password=keyring.get_password(system, username)
gis = GIS(profile=profileName)

# report time interval
d = datetime.datetime.now() - datetime.timedelta(days=1)
startTime=int(d.timestamp())*1000
endTime=int(datetime.datetime.now().timestamp())*1000
where='"startTime":{0},"endTime":{1}'.format(startTime, endTime)
payload='{"where":{'+where+'}}'

# 0. Token request
url=monitorSite+'/rest/api/auth/token'
payloadLogin = {'username': username, 'password': password}
r = requests.post(url, data = payloadLogin, verify=False)
r.raise_for_status()
token=r.json()['token']

# 1.Collections request
url=monitorSite+'/rest/api/monitor/collections'
r = requests.post(url+'?token='+token, data = '', verify=False)
r.raise_for_status()
collections=r.json()['data']

# 2. Alerts request
url=monitorSite+'/rest/api/monitor/alerts'
r = requests.post(url+'?token='+token, data = payload, verify=False)
r.raise_for_status()
alerts=r.json()

newAlerts=[]
t=datetime.datetime.fromtimestamp(alerts['time']//1000.0)
for collection in alerts['data']:
    if collection['hasAlerts']:
        collectionName=''
        for c in collections:
            if c['collectionId']==collection['collectionId']:
                collectionName=c['collectionName']
        for alertingView in collection['alertingViews']:
            counterType=alertingView['counterType']
            viewName=alertingView['name']
            for counter in alertingView['countersWithAlerts']:
                dashboardAlert={}
                counterName=counter['counterName']
                counterCategory=counter['counterCategory']
                counterInstance=counter['counterInstance']
                counterValue=counter['value']
                dashboardAlertAttributes={
                    "t":str(t),
                    "collectionName":collectionName,
                    "counterType":counterType,
                    "viewName":viewName,
                    "counterName":counterName,
                    "counterCategory":counterCategory,
                    "counterInstance":counterInstance,
                    "counterValue":str(counterValue)
                }
                dashboardAlert={"attributes":dashboardAlertAttributes}
                newAlerts.append(dashboardAlert)

# 3. Availability request
url=monitorSite+'/rest/api/monitor/availability'
r = requests.post(url+'?token='+token, data = payload, verify=False)
r.raise_for_status()
avail=r.json()

newAvailabilities=[]
t=datetime.datetime.fromtimestamp(avail['time']//1000.0)
for collection in avail['data']:
    collectionName=''
    for c in collections:
        if c['collectionId']==collection['collectionId']:
            collectionName=c['collectionName']
    availability = collection['availability']
    evalStart=availability['evalStart']
    evalEnd=availability['evalEnd']
    a=availability['availability']
    dashboardAvailAttributes={
        "t":str(t),
        "collectionName":collectionName,
        "evalStart":evalStart,
        "evalEnd":evalEnd,
        "availability":a
    }
    dashboardAvail={"attributes":dashboardAvailAttributes}
    newAvailabilities.append(dashboardAvail)

# Add records to ArcGIS Online or Portal tables (feature serivces)
item = gis.content.get(featureServiceID)

# Alerts
tableAlerts=item.tables[1]
tableAlerts.edit_features(adds = newAlerts)

# Availability
tableAvailability=item.tables[0]
tableAvailability.edit_features(adds = newAvailabilities)
