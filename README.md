# Task Manager app
This application allows you to manage your project, teams and their tasks effortlessly. Whether you're working on a small solo project or coordinating a large team, this user-friendly tool provides a centralized hub for all your project-related activities.
## Check it out!

[Task manager project deployed to Render](https://task-manager-8ugl.onrender.com/)

Username: `Billie`

Password: `5B3ytK8Av2tQKER`

## Installing

### For Windows

Install `python` and execute these commands:
```shell
git clone https://github.com/Barsh4ec/task-manager.git
cd task-manager/
python -m venv venv
venv\bin\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### For Unix-like systems
Install `python3` and execute these commands:
```shell
git clone https://github.com/Barsh4ec/task-manager.git
cd task-manager/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python3 manage.py runserver
```
## Features
* You can create multiple projects
* An ability to create multiple teams for each project
* Manage tasks for each team easily
* Filtering and searching functionality so you never get lost
## Demo
![image](https://user-images.githubusercontent.com/90793856/272357471-b37b4b0b-48bb-4164-8aa6-b8d2f2f9ec66.png)