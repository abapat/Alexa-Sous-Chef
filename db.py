import sqlite3
import os

tables = ["Create table if not exists recipe(id INTEGER PRIMARY KEY, title TEXT NOT NULL, description TEXT, cook_time TEXT, servings INTEGER, ingredients TEXT, directions TEXT, image_url TEXT, category TEXT);"]
MAX_RESULTS = 5

def main():
    initDB()

    result = getRecipe("cookie")
    for res in result:
        print(getIngredients(res[0]))
        print(getDirections(res[0]))
        print(getOtherInfo(res[0]))

    print(getOtherInfo(41435235))

def getConn():
    return sqlite3.connect("data.db")

def initDB():
    conn = getConn()
    cursor = conn.cursor()

    cursor = conn.cursor()
    for table in tables:
        cursor.execute(table)

    conn.commit()
    conn.close()

def logRecipe(title, description, cook_time, servings, ingredients, directions, image_url, category):
    conn = getConn()
    cursor = conn.cursor()

    sql = "Insert into recipe(title, description, cook_time, servings, ingredients, directions, image_url, category) values ('%s','%s','%s',%s,'%s','%s','%s', '%s');" % (title.replace("'", ""), description.replace("'", ""), cook_time.replace("'", ""), servings, ingredients.replace("'", ""), directions.replace("'", ""), image_url.replace("'", ""), category.replace("'", ""))
    #print(sql)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    conn.close()

def getRecipe(title):
    conn = getConn()
    cursor = conn.cursor()

    sql = "Select id,title from recipe where title like '%" + title + "%' limit " + str(MAX_RESULTS) + ";"

    cursor.execute(sql)
    res = cursor.fetchall()
    return res

def getIngredients(i):
    conn = getConn()
    cursor = conn.cursor()

    sql = "Select ingredients from recipe where id=%s;" % i

    cursor.execute(sql)
    res = cursor.fetchone()
    conn.close()
    if res == None:
        return res

    return res[0]

def getDirections(i):
    conn = getConn()
    cursor = conn.cursor()

    sql = "Select directions from recipe where id=%s;" % i

    cursor.execute(sql)
    res = cursor.fetchone()
    conn.close()
    if res == None:
        return res

    return res[0]

def getOtherInfo(i):
    conn = getConn()
    cursor = conn.cursor()

    sql = "Select cook_time,servings,image_url from recipe where id=%s;" % i

    cursor.execute(sql)
    res = cursor.fetchone()
    conn.close()
    return res


if __name__ == "__main__":
    main()
