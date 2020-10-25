import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question
from webos_connection import WebOsConnection

#start flask ask server
app = Flask(__name__)
ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

webosConnection = WebOsConnection()

@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("SwitchOn")
def switchOn():
    webosConnection.switchOn()
    msg = render_template('switchOn')
    return question(msg)

@ask.intent("SwitchOff")
def switchOff():
    webosConnection.switchOff()
    msg = render_template('switchOff')
    return statement(msg)

@ask.intent("SetVolume", convert={'volume': int})
def setVolume(volume):
    webosConnection.setVolume(volume)
    msg = render_template('ok')
    return question(msg)

if __name__ == '__main__':
    app.run(debug=True)