from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Skills Kit, you can say hello'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('HelloWorldIntent')
def hello_world():
    speech_text = 'Hello world'
    return statement(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

if __name__ == '__main__':
    app.run(debug=True)
