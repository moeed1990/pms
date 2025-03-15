This is a test project for Project Management System 

Installation Guide
should have python 3.11
Step 1: install python from this url https://www.python.org/downloads/release/python-3110/
Step 2: Clone the project using git clone https://github.com/moeed1990/pms.git
Step 3: Create a virtual env using this command "python -m venv pms_venv"
Step 4: Activate Environment using this command for mac "source pms_venv/bin/activate" for windows user "venv\Scripts\activate"
Step 5: installing the requirements for a project command "pip install -r requirements.txt"

To Run database requirement
python manage.py migrate

To Run Server
python manage.py runserver

To Create Superuser to access /admin/ url
python manage.py createsuperuser

Application Use
You need to signup your user account with signup/ it will logged you in automatically
you can manually sign up using /login/
you can create you project using add project button. you will be able to create as many project as you want as a owner you will be able to create project
to assign role you have to click on user management and select user, project and role. to assign the role
You can assign owner, editor and reader to a user. user can only have one role per project
When assigned user signed in they will be able to see the project as per their assigned role or they can create their own roles

Roles :
Owner: Can perform CRUD operations on the project and manage user
roles.
Editor: Can edit the project details but cannot delete the project or
manage user roles.
Reader: Can only view the project details but cannot make any changes.
No Role: Can not see the project or access it in any way, but can create their own projects


Assumption:
I assumed that user can have role so that they can access other project or they can create their own project and assigned these projects to others as well
I used custom code for roles. I was thinking about using a django permissions. but doesnot want to increase the work as per time constrain
I used bootstrap for frontend. just used the cdn so i dont have to manage the static file. how tables are not responsive as i usually use datatables for that

