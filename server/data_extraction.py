from github import Github 
import pprint 
import json
def main():
    print("Getting access token and repo from Git.json...")
    f = open("GIT.json")
    gitFile = json.load(f)
    g = Github(gitFile['token'])
    print("Done.")
    repo = g.get_repo(gitFile['repo'])
    commits = repo.get_commits().reversed
    issues = repo.get_issues().reversed
    issuesClosed = repo.get_issues(state='closed').reversed
    commitFile = open("Commit_Times.json", "w+")
    issueFile = open("Issue_times.json", "w+")
    #Getting commits and contributors 
    print("Getting list of commits and contributors... this may take a while....")
    list = {
        'repo'    : gitFile['repo'],
        'size'    : commits.totalCount , 
        'list' : {
        }
    }
    i = 0
    for commit in commits : #Extraction of dates and storing into JSON (small database) - kept locally 
        dic = { 
            'commitSha' : commit.sha,
            'time'   :  commit.commit.author.date.date().isoformat(),
            'contributor' : commit.commit.author.name
            }
        list['list'][i] = dic 
        i += 1
    #Getting issues raised
    print("Done.")
    print("Writing to Commit_Times.json...")
    json_object = json.dumps(list, indent = 4)
    commitFile.write(json_object)
    commitFile.close() 
    print("Done.")
    print("Getting issues... this may take a while...")
    issuesList = { 
                'repo'    : gitFile['repo'],
                'size'    : issues.totalCount , 
                'all issues'    : { 
                    },
                'closed issues' : {
                    
                }
                }
    i = 0
    for issue in issues : #Extraction of dates and storing into JSON (small database) - kept locally 
        dic = { 
            'start' : issue.created_at.date().isoformat(),
            }
        issuesList['all issues'][i] = dic 
        i += 1
    i = 0
    for issue in issuesClosed : #Extraction of dates and storing into JSON (small database) - kept locally 
        dic = { 
            'end' : issue.closed_at.date().isoformat(),
            }
        issuesList['closed issues'][i] = dic 
        i += 1
    json_object = json.dumps(issuesList, indent = 4)
    print("Done.")
    print("Writing to Issue_times.json...")
    issueFile.write(json_object)
    issueFile.close()
    print("Done.") 

if __name__ == '__main__':
    main()