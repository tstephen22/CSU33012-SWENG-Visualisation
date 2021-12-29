import pprint 
import json
import datetime
from datetime import date
from dateutil.rrule import rrule, MONTHLY
from collections import defaultdict 
f = open("Commit_Times.json", "r") 
visualFile = open("Visualisation_data.json", "w+")
data = json.load(f)
entrySize = data['size']
startDate = date.fromisoformat(data['list']['0']['time'])
lastEntryNo = str(entrySize-1) #Index of last commit 
endDate = date.fromisoformat(data['list'][lastEntryNo]['time'])
months = 0 
for dt in rrule(MONTHLY, dtstart=startDate, until=endDate): #Compute the amount of months
    months += 1
print (months)
#Declare data for visualisation 
visual_data = { 
        'months' : months, 
        'points' : []
        }

date = data['list']['0']['time'][:-3]
commitCount = 0 
commitWeekRate = 0;
for x in range (len(data['list'])): 
    if data['list'][str(x)]['time'][:-3] == date : 
        commitCount += 1 
    else : 
        commitWeekRate = commitCount/4
        visual_data['points'] += [{     
                                       'Date'  : date,
                                       'Count' : commitCount,
                                       'Commit Rate' : commitWeekRate
                                       }]
        date = data['list'][str(x)]['time'][:-3]
        commitCount = 0 

json_object = json.dumps(visual_data, indent = 4)
visualFile.write(json_object)
visualFile.close()
