import urllib
import re
import pprint
from food_network_wrapper import recipe_search, get_n_recipes, scrape_recipe

BASE_URL = "http://www.foodnetwork.com"
BASE_RECIPE_URL = "http://www.foodnetwork.com/recipes/a-z.html"

def main():
    '''
    dishes = scrape(baseUrl)
    for entry in dishes:
        recipe = getRecipe(entry)
        print(recipe)

    '''
    print(getNameLinks(BASE_RECIPE_URL))
    print(parseRecipes(getHTML(getLink(10, "http://www.foodnetwork.com/recipes/a-z.C.9.html"))))
    #print(ret)

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
Parses HTML for list of dishes
@return list of strings
'''
def parseRecipes(html):
    recipes = []
    match = re.search('(?s)class="group">(.*?)</div>', html)
    res = re.findall('(?s)class="arrow"><a href="(.*?)">', match.group(0))
    for r in res:
        recipes.append(BASE_URL + r)
    return recipes

'''
Gets links to all recipes- starting with A, B, C, ..., etc.
@return list of links
'''
def getNameLinks(baseUrl):
    links = []
    html = getHTML(baseUrl)
    match = re.search('(?s)a-to-z-btns">(.*?)</section>', html)
    res = re.findall('(?s)<li ><a href="(.*?)">', match.group(0))
    for r in res:
        links.append(BASE_URL + r)

    return links

'''
TODO 
Gets the maximum amount of pages (on bottom) for recipe
@return int
'''
def getNumPages(link):
    return 1

'''
Formats new link given the next page to access and the current link
ex) i= 10, http://www.foodnetwork.com/recipes/a-z.C.9.html -> http://www.foodnetwork.com/recipes/a-z.C.10.html
@return String
'''
def getLink(i, link):
    return link[:link[:link.rfind(".")].rfind(".")] + "." + str(i) + ".html" #jank af

'''
Gets a list of recipes given a search value (dish)
Returns a list of tuples: title,total time, prep time, cook time, servings, ingredients, directions

'''
def getRecipe(recipe):
    recipes = []
    results = recipe_search(recipe)
    for result in results:
        print("Scraping %s: %s" % (result.title,result.url))
        recipes.append(scrape_recipe(result.url))

    ret = []
    for r in recipes:
        ret.append((r.title, r.total_time, r.prep_time, r.cook_time, r.servings, r.ingredients, r.directions))
        print(r.categories)

    return ret

if __name__ == "__main__":
    main()

