from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, '/')

ingredients = [
'120mg water', '300g beef', '10lbs chicken', 'test', 'tesint', 'rewrwf'
]
ingredientIndex = 0

instructions = [
'1. Boil water', '2. Peel potatoes', '3. Eat potatoes'
]
instructionCounter = 1

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

@ask.intent('PickIntent', convert={'Selection' : int})
def sendIngredients(Selection):
    text = "Okay, I'm sending the ingedient list for " + str(Selection) +" to your phone."
    text += "If you'd like me to read out the ingredients, tell me to list them."
    text += "Otherwise, say Let's Cook to let me know when you have everything."
    reprompt_text += "Sory, I didn't hear what you said. Do you want me to read the ingredients or are you ready to start cooking?"
    return question(text).reprompt(reprompt_text)

@ask.intent('ListIngredients')
def listIngredients():

    text = ""
    global ingredientIndex

    if ingredientIndex == 0:
        text += render_template('ingredients', Dish=session.attributes['dish'])

    for x in range(5):
        if ingredientIndex < len(ingredients):
            text += ingredients[ingredientIndex] + ", "
            ingredientIndex += 1
        else:
            break;
    #if ingredientIndex < len(ingredients) - 1:
    #    text = text + "Say more for the next ingredients."
    #else:
    #    text = text + "Those are all the ingredients. We're ready to cook!"

    #if ingredientIndex < 5:
    #    return question(text).simple_card('Ingredients for dish ' + str(Selection), ingredients)

    return question(text)

@ask.intent("CookingIntent")
def cooking():
    text=instructions[0]
    return question(text)



@ask.intent('AMAZON.NextIntent')
def instruction():
    global instructionCounter
    if instructionCounter < len(instructions):
        text=instructions[instructionCounter]
        instructionCounter += 1
    else:
        text="No more instructions. Bon appetite!"
        return statement(text)

    return question(text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can ask me for recipes! Like, recipes for beef stew. Or, tell me how to make Philly Cheesesteaks.'
    return question(speech_text).reprompt(speech_text)

if __name__ == '__main__':
    app.run(debug=True)
