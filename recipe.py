import urllib
import re
import pprint
import db
from food_network_wrapper import recipe_search, get_n_recipes, scrape_recipe

BASE_URL = "http://www.foodnetwork.com"
BASE_RECIPE_URL = "http://www.foodnetwork.com/recipes/a-z.html"
FILTER_SYMBOLS = ["-", "with", "(", "\""]

def main():
    
    db.initDB()

    dishes = scrape(BASE_RECIPE_URL)
    for entry in dishes:
        r = getRecipe(entry)
        if r[0] != None and r[0] != "":
            try:
                db.logRecipe(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
                print("Logged %s" % r[0])
            except Exception, e:
                print("Could not log recipe for %s: %s", (r[0], str(e)))

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
Gets the maximum amount of pages (on bottom) for recipe
@return int
'''
def getNumPages(link):
    maxNum = 1
    html = getHTML(link)
    match = re.search('(?s)class="pagination">(.*?)</div>', html)
    if match == None:
        return 1
    res = re.findall('(?s)<a href=".*?">(.*?)</a>', match.group(0))
    for r in res:
        if r.isdigit() and int(r) > maxNum:
            maxNum = int(r)

    return maxNum

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
def getRecipe(url):
    print("Scraping: " + url)
    r = scrape_recipe(url)
    parsed_title, description = parseName(r.title)
    return (parsed_title, description, r.total_time, getServings(r.servings), r.ingredients, r.directions, r.picture_url, r.categories)

'''
Parses out uneeded characters from dish name
ex) Baby Back Racks (Paula Deen) -> Baby Back Racks
'''
def parseName(name):
    parsed = name
    desc = ""
    for f in FILTER_SYMBOLS:
        arr = parsed.split(f)
        if len(arr) > 1:
            desc = arr[1]
        parsed = arr[0].strip()
    return parsed, desc

def getServings(servings):
    arr = servings.split(" ")
    for a in arr:
        print(a)
        if a.isdigit():
            return int(a)
    return 1

if __name__ == "__main__":
    main()

