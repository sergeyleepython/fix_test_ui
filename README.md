UI testing
=========
Tests and tests results for https://reqres.in/

## REQUIREMENTS
Python 3.6

Python dependencies:
* pytest==3.7.1
* allure-pytest==2.5.0

## LAUNCHING
* Download drivers for browsers your need (Firefox, Chrome, Safari etc.).
* Add the paths to drivers to $PATH environment variable. You can do it temporarily:
> $ export PATH="$PATH:/path/to/driver/"
* In a terminal go to the project folder and install Python requirements:
> $ pip3 install -r requirements.txt
* Run tests specifying browser:
> $ pytest --browser firefox
