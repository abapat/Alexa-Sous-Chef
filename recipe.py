import urllib
import re

recipes = set()

def scrape(baseUrl):
    global recipes

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
    return None

'''
Gets links to all recipes- starting with A, B, C, ..., etc.
@return list of links
'''
def getNameLinks(baseUrl):
    return None

'''
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
    return None
