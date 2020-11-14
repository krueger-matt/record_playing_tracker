import config
import sqlite3
import re
from datetime import datetime

def recommendation(query):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

# Query logic: cte table is recursive: select records where play_count > 0
# and then union all with the same set of data where play_count > 1.
# Purpose of this is to get multiple rows returned if the play count is higher than 1
# This makes it so the more popular a record is, the more likely it is to be chosen
# Example from here: https://stackoverflow.com/questions/46574131/list-same-row-twice-if-the-count-is-more-than-1-in-another-column?noredirect=1&lq=1
    if query == 'most_popular':
        sql_statement = """
                        SELECT id, artist_name, album_name FROM (
                        WITH cte AS 
                        (SELECT id, artist_name, album_name, play_count
                        FROM records 
                        WHERE play_count > 0
                        AND ignore <> 1
                        UNION ALL 
                        SELECT id, artist_name, album_name, play_count - 1 
                        FROM cte 
                        WHERE play_count > 1)

                        SELECT id, artist_name, album_name, 1 AS play_count 
                        FROM cte ORDER BY id)
                        ORDER BY RANDOM() LIMIT 1;"""
    elif query == 'un_played':
        sql_statement = """SELECT id, artist_name, album_name 
                           FROM records 
                           WHERE play_count = 0
                           AND ignore <> 1
                           ORDER BY random() 
                           LIMIT 1;"""

    cur.execute(sql_statement)

    rows = cur.fetchall()

    return (rows)



# This returns a list of genres
# Albums can be categorized as multiple genres. This list just pulls the distinct individual genres
def genre():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    sql_statement = """SELECT distinct genre FROM records where ignore <> 1 ORDER BY 1"""

    cur.execute(sql_statement)

    rows = cur.fetchall()

    genre_list = []

    for row in rows:
        genre_list.append(row[0])

    genre_string = ''

    # Convert the list to a string so comma separated values can be truly split
    for x in genre_list:
        x = x +','
        genre_string += x

    genre_list = list(genre_string.split(','))
    genre_list = [x.strip(' ') for x in genre_list]

    unique_list = []

    # There are duplicates in the list after it was split, so create a new version that is only uniques
    for x in genre_list:
        if x not in unique_list:
            unique_list.append(x)

    # Sorted sorts the list from a-z
    return (sorted(unique_list))



def recommend_genre(genre):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    sql_statement = """SELECT id, artist_name, album_name 
                       FROM records 
                       WHERE genre like '%""" + genre + """%'
                       AND ignore <> 1
                       ORDER BY random() 
                       LIMIT 1;"""

    cur.execute(sql_statement)

    rows = cur.fetchall()

    return (rows)
