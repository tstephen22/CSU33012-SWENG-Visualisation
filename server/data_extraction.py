from github import Github 
import pprint 
import json

f = open("GIT.json")
gitFile = json.load(f)
g = Github(gitFile['token'])

repo = g.get_repo(gitFile['repo'])
commits = repo.get_commits().reversed
outfile = open("Commit_Times.json", "w+")
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
           'time'   :  commit.commit.author.date.date().isoformat()
           }
    list['list'][i] = dic 
    i += 1
    
json_object = json.dumps(list, indent = 4)
outfile.write(json_object)
outfile.close() 