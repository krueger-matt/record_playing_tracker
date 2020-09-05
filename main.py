import os
import sqlite3
from time import sleep
from datetime import datetime

from flask import Flask, render_template, url_for, redirect, request

import config
import functions
import forms

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY



@app.route('/')  # root : main page
def index():
    return render_template('index.html')



@app.route('/my_records/')
def my_records():
    (columns, rows) = functions.read_all('records')
    for row in rows:
        print(row)
    return render_template('my_records.html', columns=columns, rows=rows)



@app.route('/my_records_detail/')
def my_records_detail():
    (columns, rows) = functions.my_records_detail('records')
    for row in rows:
        print(row)
    return render_template('my_records_detail.html', columns=columns, rows=rows)



@app.route('/listen_to_record/<id>')
def listen_to_record(id):
    functions.listen(id)
    sleep(1)
    return redirect(url_for('my_records'))



@app.route('/un_listen_to_record/<id>')
def un_listen_to_record(id):
    functions.un_listen(id)
    sleep(1)
    return redirect(url_for('my_records'))



@app.route('/edit_record/<id>', methods=['GET', 'POST'])
def edit_record(id):
    print('id='+str(id))
    (columns, row) = functions.read_row(config.DB_NAME, 'records', id)   

    if row[5] == '':
        last_played = None
    elif row[5] is not None:
        last_played=datetime.strptime(row[5], '%Y-%m-%d')
    else:
        last_played = None

    form = forms.EditRecord(
        artist_name=row[1],
        album_name=row[2],
        genre=row[3],
        play_count=row[4],
        last_played=last_played,
        ignore=row[6],
        release_type=row[8])

    if form.is_submitted():
        result = functions.get_form_data(list(request.form.values()))
        print (result)
        functions.update_record(id, result)
        return redirect(url_for('my_records_detail',_anchor=id))

    return render_template('edit_record.html', form=form, id=id, row=row)



@app.route('/add_record/', methods=['GET', 'POST'])
def add_record(): 

    form = forms.AddRecord(
        artist_name='',
        album_name='',
        genre='',
        ignore='',
        release_type='')

    if form.is_submitted():
        result = functions.get_form_data(list(request.form.values()))
        print (result)
        functions.add_record(result)
        return redirect(url_for('my_records'))

    return render_template('add_record.html', form=form)



@app.route('/delete_record/<id>', methods=['GET', 'POST'])
def delete_record(id):
    functions.delete_record(id)
    sleep(1)
    return redirect(url_for('my_records_detail'))



if __name__ == '__main__':
    app.run(port=5000, debug=True)
