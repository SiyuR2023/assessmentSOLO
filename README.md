# assessmentSOLO
#Design
This Django application uses a responsive layout driven by the Bootstrap framework to make it easy for administrators to view user information and manage the database while giving users a better experience. The base.html template was used for all major pages to ensure consistency and code efficiency.

#Development
The project adopts Django's MTV (Model-Template-View) architecture, with models for artist, title, release year, release month, release day, format, label, genre. The views handle the application's logic, and the template classification of three categories, respectively, login class, user class and administrator class, so that you can better distinguish between ordinary users and administrators of the difference in permissions.

#Implementation
The HTML in the account folder is responsible for the login function, the HTML in the admin folder is responsible for the interface that can be logged in by accounts with administrator privileges, they include the ability to display a list of registered users and change the current album database. The HTML in the element folder is the interface that can be viewed by ordinary users, on these sites, users have the ability to access album data and view ratings given by other individuals. Once users have chosen the album they want, they may add it to their shopping basket and proceed with the purchase.

#Installation
To install and deploy

Visit PythonAnywhere and create a new app: https://www.pythonanywhere.com/

Follow this deployment guide: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject

Project URL: https://gemwxm1003.pythonanywhere.com/

Creat the basic

   pyenv local 3.7.9 
   python3 -m venv .venv # this creates the virtual environment for you
   source .venv/bin/activate # this activates the virtual environment
   pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with

    pip install Django
Project Configuration Clone the code with git clone [Git repository URL], migrate databases using python manage.py migrate, and create an admin account with python manage.py createsuperuser.

    git clone [Git repository URL]
Data Import Place CSV files in the designated folder and import them using python manage.py load_data --path [CSV file path].

    python manage.py load_data --path [CSV file path]
Execution Start the server with python manage.py runserver and navigate to http://127.0.0.1:8000/ to interact with the application.

    python3 manage.py runserver
Admin Interface Access the Django admin at http://127.0.0.1:8000/admin using the credentials created earlier.

#Functionality Introduction
The application includes dynamic data viewing, pagination for large lists, detailed views for deeper insights, user management, Multi-category search function, and a command-line tool for importing CSV data. A responsive design and an admin interface for direct database manipulation are also featured.