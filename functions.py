import config
import sqlite3
from datetime import datetime

def read_all(table):
    print('----Starting read all----')
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('PRAGMA table_info(' + str(table) + ')')
    columns = cur.fetchall()

    cur.execute('SELECT id, artist_name, album_name, play_count, last_played FROM ' + str(table) + ' ORDER BY id')

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

    cur.execute('INSERT INTO play_tracker (record_id, played_at, updated_at) values (?, ?, ?)', [int(id),datetime.now(),datetime.now()])

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

    cur.execute('UPDATE play_tracker set deleted = 1, updated_at = ? where id = (SELECT max(id) FROM play_tracker WHERE record_id = ? and deleted is null)', [datetime.now(), int(id)])

    cur.execute('UPDATE records SET play_count = ?, last_played = (SELECT max(played_at) from play_tracker where deleted is null and record_id = ?) WHERE id = ?', [new_play_count, int(id), int(id)])

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



def delete_record(id):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    cur.execute('DELETE FROM records WHERE id = ?', [id])    
    con.commit()
    con.close()



def bulk_update(values):

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('UPDATE records SET genre = ?, release_type = ? WHERE artist_name = ?', (values[1], values[2], values[0]))

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



def top_five_records():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('SELECT artist_name, album_name, play_count, last_played FROM records ORDER BY play_count DESC, last_played DESC LIMIT 5')
    rows = list(cur.fetchall())

    con.close()

    return(rows)



def top_genre():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('SELECT genre, sum(play_count) FROM records GROUP BY 1 HAVING sum(play_count) > 0 ORDER BY 2 DESC')
    genre_output = list(cur.fetchall())

    con.close()

    return(genre_output)



def read_all_filtered(values):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('PRAGMA table_info(records)')
    columns = cur.fetchall()

    b = len(values) - 1

    values = values[1:b]

    values = values.replace("'","")

    # print(values)

    values = list(values.split(", ")) 

    print(values[0])
    print(values[1])

    column_name = str(values[0])
    row_value = str(values[1])

    if column_name.lower() == 'artist name' or column_name.lower() == 'artist':
        column_name = 'artist_name'
    elif column_name.lower() == 'album name' or column_name.lower() == 'album':
        column_name = 'album_name'
    elif column_name.lower() == 'play count' or column_name.lower() == 'play' or column_name.lower() == 'count':
        column_name = 'play_count'
    elif column_name.lower() == 'last played' or column_name.lower() == 'last' or column_name.lower() == 'played':
        column_name = 'last_played'
    elif column_name.lower() == 'release type' or column_name.lower() == 'release' or column_name.lower() == 'type':
        column_name = 'release_type'
    elif column_name.lower() == 'date added' or column_name.lower() == 'added':
        column_name = 'date_added'



    cur.execute("""
        SELECT id,
                artist_name,
                album_name,
                genre,
                play_count,
                last_played
        FROM records
        WHERE """ + column_name + """ LIKE '%""" + row_value + """%'
        ORDER BY id""")

    # returns list of rows
    rows = list(cur.fetchall())

    if rows == []:
        print('table is empty :(')
    else:
        for row in rows:
            row = list(row)

    con.close()

    return (columns, rows)
