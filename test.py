import re
import httplib, urllib, base64
import defines
import json

MAX_CALORIES = 600
MAX_FAT = 30

def main():
    getHealthyRecipe("cake")

def getHealthyRecipe(name):
    rid = getRecipe(name)
    steps = getSteps(rid[0])
    ingredients = getIngredients(rid[0])
    tup = (rid[1], rid[2], rid[3], rid[4], ingredients, steps)
    print(tup)

def getRecipe(name):
    try:
        conn = httplib.HTTPSConnection('spoonacular-recipe-food-nutrition-v1.p.mashape.com')
        url = "/recipes/searchComplex?addRecipeInformation=false&fillIngredients=false&instructionsRequired=false&limitLicense=false&maxCalories=%s&maxCarbs=100&maxFat=%s&maxProtein=100&minCalories=150&minCarbs=5&minFat=5&minProtein=5&number=10&offset=0&query=%s&ranking=1" % (MAX_CALORIES, MAX_FAT, name)
        conn.request("GET", url, "{body}", defines.headers2)
        response = conn.getresponse()
        data = response.read()
        jdata = json.loads(data)
        print(jdata["results"][0])
        return (jdata["results"][0]['id'], jdata["results"][0]['title'], jdata["results"][0]['image'], jdata["results"][0]['calories'], jdata["results"][0]['fat'])
    except Exception, e:
        print(e)

    return None

def getSteps(recipeID):
    try:
        conn = httplib.HTTPSConnection('spoonacular-recipe-food-nutrition-v1.p.mashape.com')
        url = "/recipes/%s/analyzedInstructions?stepBreakdown=true" % recipeID
        conn.request("GET", url, "{body}", defines.headers2)
        response = conn.getresponse()
        data = response.read()
        jdata = json.loads(data)
        steps = []
        for step in jdata[0]['steps']:
            steps.append(step['step'])
        return steps
    except Exception, e:
        print(e)

    return None

def getIngredients(recipeID):
    try:
        conn = httplib.HTTPSConnection('spoonacular-recipe-food-nutrition-v1.p.mashape.com')
        url = "/recipes/%s/information?includeNutrition=false" % recipeID
        conn.request("GET", url, "{body}", defines.headers2)
        response = conn.getresponse()
        data = response.read()
        jdata = json.loads(data)

        ingredients = []
        arr = jdata["extendedIngredients"]
        for a in arr:
            ingredients.append(a["originalString"])
        return ingredients
    except Exception, e:
        print(e)

    return None


if __name__ == "__main__":
    main()
