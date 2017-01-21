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
    text += " Dish 1: beef stew. Dish 2: beef stroganoff. Please say the dish number you'd like to make, or say more for more options."
    reprompt_text = "I didn't catch that. What would you like to make?"
    session.attributes['dish'] = Dish
    return question(text).reprompt(reprompt_text)

@ask.intent('PickIntent', convert={'Selection': int})
def ingredient(Selection):
    text = render_template('ingredients', Selection=str(Selection))
    if Selection == 1:
        text += " one one one"

    if Selection == 2:
        text += " two two two"

    return statement(text).simple_card('Ingredients for dish ' + str(Selection), text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can ask me for recipes! Like, recipes for beef stew. Or, tell me how to make Philly Cheesesteaks.'
    return question(speech_text).reprompt(speech_text)

if __name__ == '__main__':
    app.run(debug=True)
