Notes & commands to run project


**SERVER**

py manage.py runserver

py manage.py startapp polls

// Migrate a specific app
python manage.py makemigrations polls

// General migrations
python manage.py migrate
python manage.py showmigrations

// Create superuser, winpty needed to make it interactive
winpty python manage.py createsuperuser


Apps installed:

pip install python-dotenv
pip install djangorestframework



**CLIENT**

python client_app.py


Create installer:

pyinstaller --onefile --windowed Timeclocker.py
pyinstaller --onefile --windowed --add-data ".env;." Timeclocker.py // Includes .env but didn't work


Apps installed:

pip install requests
pip install pillow
pip install psutil
pip install pyinstaller
