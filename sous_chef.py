from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement
from afg import Supervisor
from collections import OrderedDict
import db

app = Flask(__name__)
ask = Ask(app, '/')
sup = Supervisor("scenario.yaml")

ingredientIndex = 0
instructionCounter = 1

@ask.on_session_started
@sup.start
def new_session():
    app.logger.debug('new session started')

@sup.stop
def close_user_session():
    app.logger.debug("user session stopped")

@ask.session_ended
def session_ended():
    close_user_session()
    return "", 200

@ask.launch
@sup.guide
def launched():
    speech_text = 'Welcome to Sous Chef, you can ask me for recipes.'
    return question(speech_text).reprompt(speech_text)

@ask.intent('RecipeIntent')
@sup.guide
def get_recipes(Dish):
    session.attributes['dishes'] = db.getRecipe(Dish)
    text = render_template('recipe', numResults=str(len(session.attributes['dishes'])), Dish=Dish)
    for x in range(len(session.attributes['dishes'])):
        text += " Dish " + str(x) + " " + session.attributes['dishes'][x][1] + ","
    text += ". Please say the dish you'd like to make, or say more for more options."
    reprompt_text = "I didn't catch that. What would you like to make?"
    return question(text).reprompt(reprompt_text)

@ask.intent('PickIntent')
@sup.guide
def send_ingredients(Selection):
    dishesDict = OrderedDict((val.lower(), key) for (key, val) in session.attributes['dishes'])
    print Selection
    print dishesDict
    if dishesDict.get(Selection) != None:
        session.attributes['selectedDish'] = session.attributes['dishes'][dishesDict.keys().index(Selection)]
        print session.attributes['selectedDish']
        selectedDish = session.attributes['selectedDish']
    else:
        speech = "Sorry, I couldn't match what you said. Could you try again?"
        return question(speech)
    text = render_template('ingredients', Dish=selectedDish[1])
    session.attributes['ingredients'] = db.getIngredients(selectedDish[0])
    session.attributes['ingredientsList'] = session.attributes['ingredients'].split('\n')
    reprompt_text = "Sorry, I didn't hear what you said. Do you want me to read the ingredients or are you ready to start cooking?"
    return question(text).reprompt(reprompt_text).simple_card(selectedDish[1], session.attributes['ingredients'])

@ask.intent('ListIngredients')
@sup.guide
def list_ingredients():
    text = ""
    global ingredientIndex
    ingredients = session.attributes['ingredientsList']
    for x in range(5):
        if ingredientIndex < len(ingredients):
            text += ingredients[ingredientIndex] + ", "
            ingredientIndex += 1
        else:
            break;

    print ingredientIndex
    print len(ingredients)

    if ingredientIndex < len(ingredients):
        text = text + "Say more for the next ingredients."
    else:
        text = text + "Those are all the ingredients. We're ready to cook! "
        selectedDishId = session.attributes['selectedDish'][0]
        session.attributes['instructions'] = db.getDirections(selectedDishId).split('.')
        text += session.attributes['instructions'][0]

    return question(text)

@ask.intent("CookingIntent")
@sup.guide
def cooking():
    selectedDishId = session.attributes['selectedDish'][0]
    session.attributes['instructions'] = db.getDirections(selectedDishId).split('.')
    text = session.attributes['instructions'][0]
    return question(text)

@ask.intent('AMAZON.NextIntent')
def next_instruction():
    global instructionCounter
    instructions = session.attributes['instructions']
    if instructionCounter < len(instructions):
        text = instructions[instructionCounter]
        instructionCounter += 1
    else:
        done_cooking()

    return question(text)

@ask.intent('AMAZON.PreviousIntent')
def go_back():
    global instructionCounter
    instructions = session.attributes['instructions']

    if instructionCounter < 0:
        instructionCounter -= 1
        text = instructions[instructionCounter]
    else:
        text = instructions[instructionCounter] + ". This is the first step."
        instructionCounter = 0

    return question(text)

@sup.guide
def done_cooking():
    close_user_session()
    return statement(render_template('done'))

@ask.intent('AMAZON.HelpIntent')
def help():
    context_help = sup.get_help()
    return question(context_help)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    close_user_session()
    return statement(render_template('cancel'))


@ask.intent('AMAZON.StopIntent')
def stop():
    close_user_session()
    return statement(render_template('stop'))


if __name__ == '__main__':
    app.run(debug=True)
