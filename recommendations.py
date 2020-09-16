import config
import sqlite3
import re
from datetime import datetime

def recommendation(query):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    if query == 'most_popular':
        sql_statement = """SELECT artist_name, album_name 
                           FROM records 
                           WHERE play_count > (SELECT max(play_count) FROM records) - 1 
                           AND ignore <> 1
                           ORDER BY random() 
                           LIMIT 1;"""
    elif query == 'un_played':
        sql_statement = """SELECT artist_name, album_name 
                           FROM records 
                           WHERE play_count = 0
                           AND ignore <> 1
                           ORDER BY random() 
                           LIMIT 1;"""

    cur.execute(sql_statement)

    rows = cur.fetchall()

    return (rows)

def genre():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    sql_statement = """SELECT distinct genre FROM records ORDER BY 1"""

    cur.execute(sql_statement)

    rows = cur.fetchall()

    for row in rows:
        print(row[0])

    return (rows)

def recommend_genre(genre):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    sql_statement = """SELECT artist_name, album_name 
                       FROM records 
                       WHERE genre = '""" + genre + """'
                       AND ignore <> 1
                       ORDER BY random() 
                       LIMIT 1;"""

    cur.execute(sql_statement)

    rows = cur.fetchall()

    return (rows)
