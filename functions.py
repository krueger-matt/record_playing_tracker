import config
import sqlite3
from datetime import datetime

def read_all(table):
    print('----Starting read all----')
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('PRAGMA table_info(' + str(table) + ')')
    columns = cur.fetchall()

    cur.execute('SELECT id, artist_name, album_name, play_count, last_played FROM ' + str(table) + ' order by id')

    # returns list of rows
    rows = list(cur.fetchall())

    if rows == []:
        print('table is empty :(')
    else:
        for row in rows:
            row = list(row)

    con.close()

    return (columns, rows)



def my_records_detail(table):
    print('----Starting read all----')
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('PRAGMA table_info(' + str(table) + ')')
    columns = cur.fetchall()

    # returns a tuple of table names in this database
    cur.execute('SELECT * FROM ' + str(table) + ' order by id')

    # returns list of rows
    rows = list(cur.fetchall())

    if rows == []:
        print('table is empty :(')
    else:
        for row in rows:
            row = list(row)

    con.close()

    return (columns, rows)



def listen(id):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('SELECT play_count FROM records WHERE id = ?',[id])
    for row in cur:
        print (row)

    if row[0] is None:
        play_count = 0
    else:
        play_count = int(row[0])

    new_play_count = play_count + 1

    print (new_play_count)

    cur.execute('UPDATE records SET play_count = ?, last_played = ? WHERE ID = ?',
                [new_play_count, datetime.today().strftime('%Y-%m-%d'), id])

    con.commit()
    con.close()



def un_listen(id):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('SELECT play_count FROM records WHERE id = ?',[id])
    for row in cur:
        print (row)

    play_count = int(row[0])

    if play_count > 0:
        new_play_count = play_count - 1
    else:
        new_play_count = 0

    print (new_play_count)

    cur.execute('UPDATE records SET play_count = ?, last_played = ? WHERE ID = ?',
                [new_play_count, datetime.today().strftime('%Y-%m-%d'), id])

    con.commit()
    con.close()



def read_row(database, table, id):

    # Returns the column names and values for a single entry via the row id

    try:
        database = str(database)
        table = str(table)
        id = str(id)
        print(database, table, id)
    except Exception as e:
        print(e)

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('PRAGMA table_info(' + table +')')
    temp_columns = cur.fetchall()
    columns = []
    for tuple in temp_columns:
        columns.append(tuple[1])
    print(columns)

    # returns a tuple of table names in this database
    cur.execute('SELECT * FROM ' + table + ' WHERE id = ' + id)

    # returns list of rows
    row = cur.fetchall()

    if row == []:
        print('Error: No record with ID ' + id)
    else:
        print(row)

    con.close()

    return (columns, row[0]) # need to do row[0] instead of just row since the cursor returns a tuple of lists (we just need the list)



def update_record(id, new_values):

    # cur.execute can only take 2 arguments so we need to add the ID to the list
    print(new_values)

    new_values.append(id)
    print(new_values)

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('UPDATE records '
                'SET '
                'artist_name = ?, '
                'album_name = ?,'
                'genre = ?,'
                'play_count = ?,'
                'last_played = ?,'
                'ignore = ?,'
                'release_type = ?'
                'WHERE ID = ?', new_values)

    con.commit()
    con.close()



def add_record(new_values):

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('INSERT INTO records (artist_name, album_name, genre, ignore, release_type) VALUES (?,?,?,?,?)', new_values)

    con.commit()
    con.close()



def get_form_data(in_list):

    output = []

    for i in range(len(in_list) - 1):  # must be len()-1 to remove submit
        try:
            output.append(int(in_list[i]))
        except Exception as e:
            try:
                output.append(float(in_list[i]))
            except:
                output.append(in_list[i])
                continue

    return output