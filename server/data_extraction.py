from github import Github 
import pprint 
import json
g = Github("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")

repo = g.get_repo("airbnb/lottie-android") 
commits = repo.get_commits().reversed
outfile = open("Commit_Times.json", "w+")
list = {
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