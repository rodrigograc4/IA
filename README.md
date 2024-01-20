[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/yvOMUkkU)
# ia-digdug
DigDug clone for AI teaching

## How to install

*Tip: you might want to create a virtualenv first*

`$ python3 -m venv venv`

`$ source venv/bin/activate`

`$ pip install pip --upgrade`

Make sure you are running Python 3.11.

`$ pip install -r requirements.txt`

## How to play

Open 3 terminals:

`$ python3 server.py`   if needed (kill process in 8000 port):   `$ sudo lsof -t -i:8000`   -   `$ sudo kill -9 ????`

`$ python3 viewer.py`

`$ python3 student.py`

To play using the sample client make sure the client pygame hidden window has focus.

### Keys

Directions: arrows

*A*: 'a' - pump enemies

## Debug Installation

Make sure pygame is properly installed:

python -m pygame.examples.aliens

# Tested on:
- MacOS 13.6

