from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement
from afg import Supervisor
from collections import OrderedDict
import db
import re
import httplib, urllib, base64
import defines

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
    session.attributes['repeat'] = speech_text
    return question(speech_text).reprompt(speech_text)

@ask.intent('RecipeIntent')
@sup.guide
def get_recipes(Dish, Healthy):
    app.logger.debug(Dish)
    if Dish == None:
        return sup.reprompt_error

    app.logger.debug(Healthy)

    session.attributes['dishes'] = db.getRecipe(Dish)
    app.logger.debug(session.attributes['dishes'])
    dishResults = session.attributes['dishes']

    text = render_template('recipe', numResults = str(len(dishResults)), Dish = Dish)
    if len(dishResults) == 0:
        return sup.reprompt_error

    for x in range(5):
        if x < len(dishResults):
            text += " Dish " + str(x+1) + ", " + dishResults[x][1] + ","

    text += ". Please say the dish you'd like to make."
    reprompt_text = "I didn't catch that. What would you like to make?"

    options = ""
    for x in dishResults:
        options += x[1] + "\n"

    session.attributes['repeat'] = text
    return question(text).reprompt(reprompt_text).simple_card("Recipes", options)

@ask.intent('NewSearchIntent')
@sup.guide
def new_search():
    text = "Okay, let's try some new recipes. Please tell me your new search."
    return question(text)

@ask.intent('OptionsIntent')
@sup.guide
def return_to_options():
    options = ""
    for x in session.attributes['dishes']:
        options += x[1] + ". \n"
    return question(options)

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
    imageUrl = getThumbnail(selectedDish[1])
    imageUrl = imageUrl.replace("\\", "")
    session.attributes['repeat'] = text
    return question(text).standard_card(selectedDish[1], session.attributes['ingredients'], imageUrl, imageUrl)

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
    elif text == "":
        return cooking()

    session.attributes['repeat'] = text
    return question(text)

@ask.intent("CookingIntent")
@sup.guide
def cooking():
    text = "Alright, we're ready to cook! "
    selectedDishId = session.attributes['selectedDish'][0]
    session.attributes['instructions'] = db.getDirections(selectedDishId).split('.')
    text += session.attributes['instructions'][0]

    session.attributes['repeat'] = text
    return question(text)

@ask.intent('AMAZON.NextIntent')
@sup.guide
def next_instruction():
    global instructionCounter
    instructions = session.attributes['instructions']
    if instructionCounter < len(instructions) - 1:
        text = instructions[instructionCounter]
        instructionCounter += 1
    else:
        return done_cooking()

    session.attributes['repeat'] = text
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

    session.attributes['repeat'] = text
    return question(text)

@sup.guide
def done_cooking():
    close_user_session()
    return statement(render_template('done'))

@ask.intent('AMAZON.HelpIntent')
def help():
    context_help = sup.get_help()
    session.attributes['repeat'] = context_help
    return question(context_help)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    close_user_session()
    return statement(render_template('cancel'))


@ask.intent('AMAZON.StopIntent')
def stop():
    close_user_session()
    return statement(render_template('stop'))

@ask.intent('AMAZON.RepeatIntent')
def repeat():
    app.logger.debug(session.attributes['repeat'])
    return question(session.attributes['repeat'])

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


def getThumbnail(title):
    params = urllib.urlencode({
        # Request parameters
        'q': title,
        'count': '1',
        'offset': '0',
        'mkt': 'en-us',
        'safeSearch': 'Moderate',
    })

    try:
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", defines.headers)
        response = conn.getresponse()
        data = response.read()
        res = re.findall('"thumbnailUrl": "(.*?)"', data)
        conn.close()
        if res == None:
            return None
        return res[0]
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(debug=True)
