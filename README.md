Gathers World of Warcraft character information for all characters provided in the config file.  
Saves character information to a database and displays it on a webpage using Flask.  
Click the characters name it will open a new tab taking you to their raider.io profile


# Set up 
Go to the directory and **pip install -r requirements.txt** 

Edit config.ini to include your own Client ID and Secret (https://develop.battle.net/documentation/guides/using-oauth).

Edit config.ini to include characters you are interested in seeing (name, server, region).

# Use
Go to the working directory where you saved the files and run app.py.  
Open your browser and go to http://127.0.0.1:5000/

![Example Image](/example.png)



