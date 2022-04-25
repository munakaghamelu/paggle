# Paggle

An Interface Connecting ML Models With Encrypted Medical Data.

![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)

# Abstract

There are a number of problems in the field of health and medicine that can be solved with technology. However, trying to apply technological innovations,
such as machine learning, to solve these problems is troublesome. The research aspect of this project was to determine whether it was possible maintain the integrity and sensitivity of encrypted medical data through a system accessible by many users. This was proven by firstly presenting an encryption script that uses python’s fernet library to encrypt the mock sensitive data. Then the robustness of the system was proven by a failed hacking attempt, in which a mock malicious python script was written to try to extract the sensitive data once it was decrypted inside the part of the system not accessible to the user. Further, the research phase presents various case studies on why Machine Learning and Health Data are such interesting parallels to intertwine. Regarding the development part of this project, the main contributions made was a system called Paggle. Paggle is a MVP that has a database that is able to be injected with encrypted medical data and then presented to user upon a specific dataset request. Paggle takes a unique approach by utilising the security and isolated merits that
come as a result of using a docker container. Upon successful execution of a ML model within Paggle’s dockerised models container, a confusion matrix and other useful metrics are presented to illustrate how well a model has performed. Paggle itself is an interface that has been designed with accessibility and usability in mind. Paggle is an Open Source.

# Paggle User Manual

## Steps to Startup Paggle

1. Activate django-env virtual environment

```bash
clone https://github.com/munakaghamelu/paggle.git
cd paggle
source django-env/bin/activate
```

2. Install requirements.txt into django-env

```bash
pip install -r requirements.txt
````

3. Runserver to start Paggle in localhost

```
python3 paggle/manage.py runserver
```

## Possible errors and fixes

1. No superuser to access paggle database -> Create superuser

Default superuser login is: username: muna, password: testing321

To create a new superuser, type following command to terminal:

```
python manage.py createsuperuser
```

2. Making changes to appilication models -> Migrate changes to Django Sqlite db

```
python manage.py makemigrations
python manage.py migrate
```

3. Problems with Django, Docker or Python -> Read documentation, Django YouTube tutorial

- https://docs.djangoproject.com/en/4.0/
- https://docs.docker.com/
- https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&ab_channel=CoreySchafer
