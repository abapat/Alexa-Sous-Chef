import urllib

def getHTML(url):
    f = urllib.urlopen(url)
    return f.read()