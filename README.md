VISUALISATION PROJECT - Theo Stephens Kehoe - Student No.: 19334945 

Uploading as .zip as I had some problems with committing to old repository. 

Description of Project: 
This application provides a visualisation of the commit rate of a repository over time. The commit rate is defined
as the average amount of commits made per week for a given month for a repository. This metric is useful as it allows 
software engineers to see trends in how often they commit to a repository and to see if there is any general trends 
between the commit rate and other metrics. This application, for example, lets you see if there are any trends between 
the commit rate and issues raised for a repository/project. 

The application also provides a breakdown of the the top contributors of a repository and the amount of commits they have made - 
a useful metric as it allows us to see who is making the most impact on the repository. The metric is also useful as it allows
us to see whether most work done for a project is done by a few large contributors or many small contributors. 

Calculation for commit rate: 
Commit rate = Total commits for the month / 4 

Requirements to run:
For server:
-Python 
-Python packages PyGithub, Flask and python-dateutil
For client: 
-Nodejs 
-npm 

Simple install (if on windows): 
-Unzip into folder
-Run INSTALL.bat 
-If 'python' is not recognised as a command, edit INSTALL.bat and replace with 'py' - it is 
also possible to just replace each occurence with "python -m pip install [package]" 
To install client manually, cd into 'client' folder and run "npm install".

To RUN: 
-After installing, run RUN.bat. If the client or server fails individually, you can 
manually start them up using either StartClient.bat or StartServer.bat. 
-Same as the install guide, if 'python' is not recognised in the .bat then replace each occurence with 'py' 
or whatever is used to run python in your cmd. 

To manually enter the repository for viewing (as well as specificing the access token), please edit the GIT.json 
located in /server. 

If any help is needed please feel free to contact me. 

NOTE*: I am very new to coding in React / javascript as well as Python, so I apologise if my coding standards are not 
correct for the languages. 

Tools / Libraries used: 
-Python
-PyGithub
-Flask for backend
-React for front end
-ReCharts 
-Material UI 

