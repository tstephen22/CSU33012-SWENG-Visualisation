import pprint 
import json
import datetime
from datetime import date
from dateutil.rrule import rrule, MONTHLY
from collections import defaultdict 
from dateutil.relativedelta import relativedelta

def main():
    MIN_DISPLAY_COMMITS = 50

    f = open("Commit_Times.json", "r") 
    visualFile = open("Visualisation_data.json", "w+")
    commitData = json.load(f)
    print(commitData['size'])
    l = open("Issue_times.json", "r")
    issueData = json.load(l)

    authorVisFile = open("Author_visualisation.json", "w+")
    othersVisFile = open("Other_visualisation.json", "w+")

    commitSize = commitData['size']
    startDate = date.fromisoformat(commitData['list']['0']['time'])
    lastEntryNo = str(commitSize-1) #Index of last commit 
    endDate = date.fromisoformat(commitData['list'][lastEntryNo]['time'])
    if(startDate.isoformat == endDate.isoformat): 
        endDate = startDate + relativedelta(months=1)
    commitMonths = 0 
    issueMonths = 0
    avgCommitRate = 0
    #Declare commit data for visualisation
    commit_visual = { 
            'Repository Name': commitData['repo'],
            'Commit months' : commitMonths,
            'Issue months'  : issueMonths, 
            'TotalCommits'  : commitSize,
            'avgCommitRate' : avgCommitRate, 
            'points' : []
            }
    for dt in rrule(MONTHLY, dtstart=startDate, until=endDate): #Compute the amount of months
        isoForm = dt.date().isoformat()[:-3]
        commitMonths += 1
        commit_visual['points'] += [{     
                                        'Date'  : isoForm,
                                        'Commit Count' : 0,
                                        'Commit Rate' : 0, 
                                        'Total Issue Count' : 0,
                                        'Issues opened' : 0,
                                        'Issues closed' : 0
                                        }]
    commit_visual['Commit months'] = commitMonths
    date1 = commitData['list']['0']['time'][:-3]
    commitCount = 0 
    commitWeekRate = 0;
    issueCount = 0 

    def getIndex(list, item): 
        for x in range (len(list)): 
            if (list[x]['Date'] == item):
                return x
        return -1;
            
    for x in range (len(commitData['list'])): 
        if commitData['list'][str(x)]['time'][:-3] == date1 : 
            commitCount += 1 
        else : 
            commitWeekRate = commitCount/4
            index = getIndex(commit_visual['points'], date1)
            commit_visual['points'][index]['Commit Rate'] = commitWeekRate
            commit_visual['points'][index]['Commit Count'] = commitWeekRate
            date1 = commitData['list'][str(x)]['time'][:-3]
            commitCount = 0 

    entrySize = issueData['size']
    if entrySize != 0 : 
        startDate = date.fromisoformat(issueData['all issues']['0']['start'])
        lastEntryNo = str(entrySize-1) #Index of last commit 
        endDate = date.fromisoformat(issueData['all issues'][lastEntryNo]['start'])
        issueMonths = 0 
        for dt in rrule(MONTHLY, dtstart=startDate, until=endDate): #Compute the amount of months
            issueMonths += 1
        commit_visual['Issue Months'] = issueMonths
        #Get all issues
        date1 = issueData['all issues']['0']['start'][:-3]
        issueCount = 0 
        #Calculating opening of issues and setting total count
        for x in range (len(issueData['all issues'])): 
            if issueData['all issues'][str(x)]['start'][:-3] == date1 : 
                issueCount += 1 
            else : 
                index = getIndex(commit_visual['points'], date1)
                commit_visual['points'][index]['Total Issue Count'] = issueCount
                commit_visual['points'][index]['Issues opened'] = issueCount
                date1 = issueData['all issues'][str(x)]['start'][:-3]
                issueCount = 0
        #Entering in number of closed issues per month       
        date1 = issueData['closed issues']['0']['end'][:-3]
        closedCount = 0
        for x in range (len(issueData['closed issues'])): 
            if issueData['closed issues'][str(x)]['end'][:-3] == date1 : 
                closedCount += 1 
            else : 
                index = getIndex(commit_visual['points'], date1)
                commit_visual['points'][index]['Issues closed'] = closedCount
                date1 = issueData['all issues'][str(x)]['start'][:-3]
                issueCount = 0
        #Subtracting closed issues from total count of issues 
        for x in range (len(issueData['closed issues'])):
            for y in range (len(commit_visual['points'])):
                if (commit_visual['points'][y]['Date'] == issueData['closed issues'][str(x)]['end'][:-3]): 
                    if(commit_visual['points'][y]['Total Issue Count'] != 0):
                        commit_visual['points'][y]['Total Issue Count'] -= 1
                    break; 

    for x in commit_visual['points']: 
        avgCommitRate += x['Commit Rate']
    avgCommitRate /= commit_visual['Commit months']
    
    commit_visual['avgCommitRate'] = avgCommitRate
    json_object = json.dumps(commit_visual, indent = 4)
    visualFile.write(json_object)
    visualFile.close()

    #Counting authors in commit 
    def findContrib(list, contributor): 
        for x in range (len(list)):
            if(list[x]['contributor'] == contributor):
                return x
        return -1; 

    author_visual = { 
            'Repository Name': commitData['repo'],
            'points' : [{
                            'contributor' : "others",
                            'count'       : 0
            }]
            }

    others_visual = { 
            'Repository Name': commitData['repo'],
            'Minium cut off for commits' : MIN_DISPLAY_COMMITS*(0.05),
            'points' : []
            }
    for x in range (len(commitData['list'])): 
        contributor = commitData['list'][str(x)]['contributor']
        if(findContrib(author_visual['points'], contributor) == -1): 
            author_visual['points'] += [{
                                    'contributor' : contributor,
                                    'count'       : 1
            }]
        else : 
            index = findContrib(author_visual['points'], contributor)
            author_visual['points'][index]['count'] += 1

    #Others pie chart
    print(commitSize)
    if commitSize >= MIN_DISPLAY_COMMITS:  #Only include 'others' contributor if number of commits exceeds MIN_DISPLAY_COMMITS (default is 50)
        author_visual_updated = { 
            'Repository Name': commitData['repo'],
            'points' : [{
                            'contributor' : "Others",
                            'count'       : 0
            }]
            }
        for x in author_visual['points']: 
            if (x['count'] <= (MIN_DISPLAY_COMMITS*(0.1))): #If commit of contributor is less than 5% of MIN_DISPLAY_COMMITS, then put into others
                author_visual_updated['points'][0]['count'] +=  x['count'] #Element 0 of points list is the 'others' contributor 
                others_visual['points'] += [{
                                    'contributor' : x['contributor'],
                                    'count'       : x['count']
                }]
            else: 
                author_visual_updated['points'] += [{
                                    'contributor' : x['contributor'],
                                    'count'       : x['count']
                }]
        author_visual = author_visual_updated

    json_object = json.dumps(others_visual, indent = 4)
    othersVisFile.write(json_object)
    othersVisFile.close()

    json_object = json.dumps(author_visual, indent = 4)
    authorVisFile.write(json_object)
    authorVisFile.close()
    
if __name__ == '__main__':
    main()