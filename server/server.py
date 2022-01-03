import data_extraction
import data_manipulation
from github import Github
from github import GithubException 
from flask import request
from flask import Response
from flask import Flask 
import json
app = Flask(__name__)

@app.route("/commits")
def commits():
    f = open("Visualisation_data.json")
    data = json.load(f)
    return data

@app.route("/authors")
def issues():
    f = open("Author_visualisation.json")
    data = json.load(f)
    return data 
 
@app.route("/other_authors")
def other_authors():
    f = open("Other_visualisation.json")
    data = json.load(f)
    return data 

@app.route("/add", methods=['POST'])
def add(): 
    print('Recieved from client:{}'.format(request.data))
    responseDict = { 
                    'response' : ""
                    }
    responseToClient = ""
    data = request.json
    newToken = data['send']['authKey']
    newRepo = data['send']['repo']
    
    try: 
        g = Github(newToken)
    except GithubException as e: 
        print("Token " + newToken + " unaccessible / non-existentant")
        responseDict['response'] = "Token error"
        response = json.dumps(responseDict)
        return Response(response)
    
    try: 
        repo = g.get_repo(newRepo) 
    except GithubException as e:
        print("Repo " + newRepo + " unaccessible / non-existentant")
        responseDict['response'] = "Repo error"
        response = json.dumps(responseDict)
        return Response(response)
    #If it passes the two tries, it is a valid repo and token
    #Writing out to json file   
    f = open("GIT.json", "r")
    gitFile = json.load(f)
    gitFile['repo'] = newRepo
    gitFile['token'] = newToken
    f = open("GIT.json", "w")
    f.write(json.dumps(gitFile))
    f.close()
    #Running extraction
    data_extraction.main() 
    data_manipulation.main()
    #Sending success response 
    dict = {
            'response' : "success"
     }
    response = json.dumps(dict)
    return Response(response)
     
if __name__ == "__main__":
    app.run(debug=True)
