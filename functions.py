import config
import sqlite3
import re
from datetime import datetime

def read_all():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('PRAGMA table_info(records)')
    columns = cur.fetchall()

    cur.execute("""SELECT id, 
                          artist_name, 
                          album_name, 
                          play_count, 
                          last_played 
                   FROM records 
                   ORDER BY artist_name, sort_order""")

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
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('PRAGMA table_info(' + str(table) + ')')
    columns = cur.fetchall()

    # returns a tuple of table names in this database
    cur.execute('SELECT * FROM ' + str(table) + ' ORDER BY artist_name, sort_order')

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
                'release_type = ?,'
                'sort_order = ?'
                'WHERE ID = ?', new_values)

    con.commit()
    con.close()



def add_record(new_values):

    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute("""INSERT INTO records (artist_name, album_name, genre, ignore, release_type, date_added) VALUES (?,?,?,?,?,date('now'))""", new_values)
    # cur.execute('UPDATE records SET date_added = date('now') WHERE id = (SELECT max(id) from records)')

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

    return (rows)



def top_five_artists():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('SELECT artist_name, sum(play_count) FROM records GROUP BY 1 HAVING sum(play_count) > 0 ORDER BY 2 DESC LIMIT 5')
    rows = list(cur.fetchall())

    con.close()

    return (rows)



def top_genre():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('SELECT genre, sum(play_count) FROM records GROUP BY 1 HAVING sum(play_count) > 0 ORDER BY 2 DESC')
    genre_output = list(cur.fetchall())

    con.close()

    return (genre_output)



def read_all_filtered(values):
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()

    cur.execute('PRAGMA table_info(records)')
    columns = cur.fetchall()

    b = len(values) - 1

    values = values[1:b]

    values = values.replace("'","")

    values = list(values.split(", ")) 

    print(values[0])
    print(values[1])
    print(values[2])
    print(values[3])

    column_name = str(values[0])
    row_value = str(values[1])
    column_name_2 = str(values[2])
    row_value_2 = str(values[3])

    greater = '>'
    less = '<'
    equal = '='
    operator = """ LIKE '%"""
    operator_close = """%'"""
    operator_2 = """ LIKE '%"""
    operator_close_2 = """%'"""

# -------------- WHERE CLAUSE --------------
    if len(column_name) > 0:
        # Correct user friendly column name into database column name
        column_name = column_name.lower().replace(' ', '_')

        # Allow >, <, = for play_count, last_played, and date_added filters
        if column_name == 'play_count' or column_name == 'id':
            if greater in row_value or less in row_value or equal in row_value:
                operator = ' '
                operator_close = ' '
        elif column_name == 'last_played' or column_name == 'date_added':
            print('Starting row_value: '+ row_value)
            if greater in row_value:
                operator = greater
                row_value = row_value.replace('>','')
            elif less in row_value:
                operator = less
                row_value = row_value.replace('<','')
            elif equal in row_value:
                operator = equal
                row_value = row_value.replace('=','')
            else:
                operator = equal

            operator_close = ''
            row_value = row_value.strip()
            row_value = "'" + row_value + "'"

            print("Operator: " + str(operator))
            print('New row_value: ' + row_value)

        where_clause = 'WHERE ' + column_name + operator + row_value + operator_close
    else:
        where_clause = ''

    # -------------- AND CLAUSE --------------
    if len(column_name_2) > 0:
        column_name_2 = column_name_2.lower().replace(' ', '_')

        # Allow >, <, = for play_count, last_played, and date_added filters
        if column_name_2 == 'play_count' or column_name_2 == 'id':
            if greater in row_value_2 or less in row_value_2 or equal in row_value_2:
                operator_2 = ' '
                operator_close_2 = ' '
        elif column_name_2 == 'last_played' or column_name_2 == 'date_added':
            print('Starting row_value_2: '+ row_value_2)
            if greater in row_value_2:
                operator_2 = greater
                row_value_2 = row_value_2.replace('>','')
            elif less in row_value_2:
                operator_2 = less
                row_value_2 = row_value_2.replace('<','')
            elif equal in row_value_2:
                operator_2 = equal
                row_value_2 = row_value_2.replace('=','')
            else:
                operator_2 = equal

            operator_close_2 = ''
            row_value_2 = row_value_2.strip()
            row_value_2 = "'" + row_value_2 + "'"

            print("Operator: " + str(operator_2))
            print('New row_value_2: ' + row_value_2)

        and_clause = ' AND ' + column_name_2 + operator_2 + row_value_2 + operator_close_2
    else:
        and_clause = ''

    sql_statement = """
        SELECT id,
                artist_name,
                album_name,
                genre,
                play_count,
                last_played
        FROM records
        """ + where_clause + and_clause + """
        ORDER BY id"""

    print(sql_statement)

    cur.execute(sql_statement)

    # returns list of rows
    rows = list(cur.fetchall())

    if rows == []:
        print('table is empty :(')
    else:
        for row in rows:
            row = list(row)

    # Count records returned
    cursor = con.execute("""SELECT COUNT(*) FROM records """ + where_clause + and_clause)

    for value in cursor:
        count_of_records = int(value[0])
        print(count_of_records)

    con.close()

    return (columns, rows, count_of_records)
