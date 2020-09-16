import os
import sqlite3
from time import sleep
from datetime import datetime

from flask import Flask, render_template, url_for, redirect, request

import config
import functions
import recommendations
import forms

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY



@app.route('/')  # root : main page
def index():
    mprows = [('','')]
    uprows = [('','')]
    grows = [('','')]

    return render_template('index.html', mprows=mprows, uprows=uprows, grows=grows)



@app.route('/most_popular/')
def most_popular():
    mprows = recommendations.recommendation('most_popular')
    uprows = [('','')]
    grows = [('','')]
    sleep(1)
    # return redirect(url_for('index.html', rows=rows))
    return render_template('index.html', mprows=mprows, uprows=uprows, grows=grows)



@app.route('/un_played/')
def un_played():
    mprows = [('','')]
    uprows = recommendations.recommendation('un_played')
    grows = [('','')]
    sleep(1)
    # return redirect(url_for('index.html', rows=rows))
    return render_template('index.html', mprows=mprows, uprows=uprows, grows=grows)



@app.route('/genre', methods=['GET', 'POST'])
def genre():
    form = forms.RecommendGenre()
    genre_result = recommendations.genre()
    genre_list = []
    for row in genre_result:
        genre_list.append(row[0])
    print (genre_list)
    form.choice.choices = genre_list
    mprows = [('','')]
    uprows = [('','')]
    grows = [('','')]
    sleep(1)

    if form.is_submitted():
        result = functions.get_form_data(list(request.form.values()))
        print(result)
        genre = result[0]
        grows = recommendations.recommend_genre(genre)
        return render_template('index.html', mprows=mprows, uprows=uprows, grows=grows, form=form)

    return render_template('genre.html', mprows=mprows, uprows=uprows, grows=grows, form=form)



@app.route('/my_records/')
def my_records():
    (columns, rows) = functions.read_all()
    return render_template('my_records.html', columns=columns, rows=rows)



@app.route('/my_records_detail/')
def my_records_detail():
    (columns, rows) = functions.my_records_detail('records')
    return render_template('my_records_detail.html', columns=columns, rows=rows)



@app.route('/listen_to_record/<id>')
def listen_to_record(id):
    functions.listen(id)
    sleep(1)
    return redirect(url_for('my_records',_anchor=id))



@app.route('/un_listen_to_record/<id>')
def un_listen_to_record(id):
    functions.un_listen(id)
    sleep(1)
    return redirect(url_for('my_records',_anchor=id))



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



@app.route('/bulk_update/', methods=['GET', 'POST'])
def bulk_update():
    form = forms.BulkUpdate(
        artist_name='',
        genre='',
        release_type='')

    if form.is_submitted():
        result = functions.get_form_data(list(request.form.values()))
        print (result)
        functions.bulk_update(result)   
        return redirect(url_for('my_records_detail'))

    return render_template('bulk_update.html', form=form)



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



@app.route('/stats/')
def stats():
    rows = functions.top_five_records()
    for row in rows:
        print(row)

    genre_output = functions.top_genre()
    for row in genre_output:
        print(genre_output)

    artists = functions.top_five_artists()
    for row in artists:
        print(artists)

    return render_template('stats.html', rows=rows, genre_output=genre_output, artists=artists)



@app.route('/filters/', methods=['GET', 'POST'])
def filters():

    form = forms.Filters(
        column_name='',
        row_value='',
        column_name_2='',
        row_value_2='')

    if form.is_submitted():
        result = functions.get_form_data(list(request.form.values()))
        print ("result: " + str(result))
        return redirect(url_for('my_records_filtered', result=result))

    return render_template('filters.html', form=form)



@app.route('/my_records_filtered/<result>', methods=['GET', 'POST'])
def my_records_filtered(result):

    print("My Records Filtered Result: " + str(result))

    (columns, rows, count_of_records) = functions.read_all_filtered(result)

    return render_template('my_records_filtered.html', columns=columns, rows=rows, count_of_records=count_of_records)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
