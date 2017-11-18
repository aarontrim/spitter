# spitter
### Simple Django Twitter Clone
##### _Aaron Trim 2017_
###### App Specification
Spitter is a Python + Django web application. It contains some basic social media functionalities, namely:
* User registration and login
* Ability to customise profile with username, biography, and uploaded profile image
* View other users profiles through either directly linking of a known username, the discover page, or links from other pages
* Create 'spitts', short messages that are broadcast to your entire network of followers
* Follow people and see who is following you, your home page will show your spitts as well as those of the people you are following

###### Usage
Spitter is written in Python 3 using the Django framework. As required edit the settings.py to point to your hosts and secret key locations.A simple way to launch the server is given in the bash script runserver.sh, running the same command on Windows should yield the same results. Ensure to run
```
pip install -r requirements.txt
```
As always before launching the Python application.
Otherwise usage is similar to all other Django applications, see [here](https://docs.djangoproject.com/en/1.11/) for more information.