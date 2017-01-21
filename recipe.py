import urllib
import re
from food_network_wrapper import recipe_search, get_n_recipes, scrape_recipe

BASE_URL = "http://www.foodnetwork.com/recipes/a-z.html"

if __name__ == "__main__":
    main()

def main():
    dishes = scrape(baseUrl)
    for entry in dishes:
        recipe = getRecipe(entry)
        print(recipe)

'''
Scrapes Food Network starting at baseUrl for a list of dishes
@returns set of Strings
'''
def scrape(baseUrl):
    recipes = set()

    for link in getNameLinks(baseUrl):
        numPages = getNumPages(link)
        for i in range(1, numPages):
            nextLink = getLink(i, link)
            html = getHTML(nextLink)
            dishes = parseRecipes(html)
            for d in dishes:
                recipes.add(d)

    for recipe in recipes:
        print recipe

    return recipes


'''
Gets HTML of a specified url
@return String
'''
def getHTML(url):
    f = urllib.urlopen(url)
    return f.read()


'''
TODO
Parses HTML for list of dishes
@return list of strings
'''
def parseRecipes(html):
    return None

'''
TODO
Gets links to all recipes- starting with A, B, C, ..., etc.
@return list of links
'''
def getNameLinks(baseUrl):
    return None

'''
TODO
Gets the maximum amount of pages (on bottom) for recipe
@return int
'''
def getNumPages(link):
    return 1

'''
TODO
Formats new link given the next page to access and the current link
ex) i= 10, http://www.foodnetwork.com/recipes/a-z.C.9.html -> http://www.foodnetwork.com/recipes/a-z.C.10.html
@return String
'''
def getLink(i, link):
    return None

'''
Gets a list of recipes given a search value (dish)
Returns a list of tuples: title,total time, prep time, cook time, servings, ingredients, directions

'''
def getRecipe(recipe):
    recipes = []
    results = recipe_search(recipe)
    for result in results:
        print("Scraping %s: %s" % (i.title,i.url))
        recipes.append(scrape_recipe(i.url))

    ret = []
    for r in recipes:
        ret.append((r.i.title, r.total_time, r.prep_time, r.cook_time, r.servings, r.ingredients, r.directions))

    return ret
