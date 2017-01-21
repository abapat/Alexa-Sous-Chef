from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement
from afg import Supervisor
from collections import OrderedDict
import db
import re

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
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text)

@ask.intent('RecipeIntent')
@sup.guide
def get_recipes(Dish):
    app.logger.debug(Dish)
    if Dish == None:
        return sup.reprompt_error

    session.attributes['dishes'] = db.getRecipe(Dish)
    app.logger.debug(session.attributes['dishes'])
    dishResults = session.attributes['dishes']
    text = render_template('recipe', numResults = str(len(dishResults)), Dish = Dish)

    for x in range(len(dishResults)):
        text += " Dish " + str(x+1) + " " + dishResults[x][1] + ","

    text += ". Please say the dish you'd like to make, or say more for more options."
    reprompt_text = "I didn't catch that. What would you like to make?"

    options = ""
    for x in dishResults:
        options += x[1] + "\n"

    return question(text).reprompt(reprompt_text).simple_card("Recipes", options)

@ask.intent('PickIntent')
@sup.guide
def send_ingredients(Selection):
    selectedTuple = searchRecipe(session.attributes['dishes'], Selection)
    print selectedTuple

    if selectedTuple == None:
        return sup.reprompt_error

    session.attributes['selectedDish'] = selectedTuple
    selectedDish = selectedTuple
    text = render_template('ingredients', Dish=selectedDish[1])
    session.attributes['ingredients'] = db.getIngredients(selectedDish[0])
    session.attributes['ingredientsList'] = session.attributes['ingredients'].split('\n')
    app.logger.debug("getting other")
    otherInfo = db.getOtherInfo(selectedDish[0])
    app.logger.debug(otherInfo)
    selectedDishImage = otherInfo[2]
    return question(text).simple_card(selectedDish[1], session.attributes['ingredients'])

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
        cooking()

    return question(text)

@ask.intent("CookingIntent")
@sup.guide
def cooking():
    selectedDishId = session.attributes['selectedDish'][0]
    session.attributes['instructions'] = db.getDirections(selectedDishId).split('.')
    text = session.attributes['instructions'][0]
    return question(text)

@ask.intent('AMAZON.NextIntent')
@sup.guide
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
@sup.guide
def previous_instruction():
    global instructionCounter
    instructions = session.attributes['instructions']

    if instructionCounter > 0:
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

###helper methods
def searchRecipe(tupRecipes, searchTerm):
    #try exact match first
    for tup in tupRecipes:
        if searchTerm.lower() == tup[1].lower:
            return tup

    #now try case insensitive substrings
    for tup in tupRecipes:
        if re.search(searchTerm, tup[1], re.IGNORECASE):
            return tup
    return None


if __name__ == '__main__':
    app.run(debug=True)
