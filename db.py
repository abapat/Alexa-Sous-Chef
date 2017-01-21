import sqlite3
import os

tables = ["Create table if not exists recipe(id INTEGER PRIMARY KEY, title TEXT NOT NULL, description TEXT, cook_time TEXT, servings INTEGER, ingredients TEXT, directions TEXT, image_url TEXT, category TEXT);"]

def main():
    initDB()

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

def getRecipe(dish):
    conn = getConn()
    cursor = conn.cursor()

    sql = "Select * from recipe where title like '%" + dish + "%';"
    print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res

if __name__ == "__main__":
    main()

