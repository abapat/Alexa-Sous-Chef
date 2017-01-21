from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launch():
    speech_text = 'Welcome to Sous Chef, you can ask me for recipes.'
    return question(speech_text).reprompt(speech_text)

@ask.intent('RecipeIntent')
def recipe(Dish):
    text = render_template('recipe', Dish=Dish)
    text += " Which would you like?"
    reprompt_text = "I didn't catch that. What would you like to make?"
    return question(text).reprompt(reprompt_text)

@ask.intent('PickIntent')
def ingredient(Selection):
    text = render_template('ingredients', Selection=Selection)
    return statement(text).simple_card('Ingredients for ' + Selection, text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can ask me for recipes!'
    return question(speech_text).reprompt(speech_text)

if __name__ == '__main__':
    app.run(debug=True)
