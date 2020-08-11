# monitor-report-to-dashboard
Sample to Read data from ArcGIS Monitor API and store it to ArcGIS Online or ArcGIS Enterprise Portal for Dashboard access

# How to Deploy

## 1. Feature Service

Publish "MonitorDashboard" Feature Service to Portal or Online by Content: Add Item

* MonitorDashboard.gdb.zip (file geodatabase)

Write down itemid of the service, that will be needed later at the config.


## 2. ArcGIS API for Python

https://developers.arcgis.com/python/guide/install-and-set-up/

* https://repo.anaconda.com/archive/Anaconda3-2020.02-Windows-x86_64.exe
* (Anaconda Prompt) conda install -c esri arcgis


## 3. Configure credentials

* (Anaconda Prompt) Python

Create credentials to keyring with your ArcGIS Monitor user that is used to read data
```python
import keyring
keyring.set_password("ArcGIS_Monitor", "username", "password")
```

Create profile for your ArcGIS Online or Portal member that is used to write data
```python
from arcgis.gis import GIS
dashboard = GIS(url="https://arcgis.com/", username='arcgis_python', password="P@ssword123", profile="dashboard")
```

## 4. Setup scheduled task

### Download and configure Command (.bat) and Script (.py) files

* MonitorReportToDashboard.bat
* MonitorReportToDashboard.py

Edit files according to your path and settings

```
# ArcGIS Monitor:
monitorSite='https://mymonitor.domain.local'
username="dashboard"

# ArcGIS Feature Services
featureServiceID="itemid"

# Constant variables
system="ArcGIS_Monitor"
profileName = "dashboard"
```

### Import or configure scheduled task

Task Scheduler, import

* MonitorReportToDashboard.xml

Action: MonitorReportToDashboard.bat

Run every day, repeat every 1 hour
