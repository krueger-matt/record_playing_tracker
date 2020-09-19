from flask_wtf import FlaskForm
import wtforms as wt
from wtforms.fields import html5 as wt5
from datetime import datetime
import functions



class EditRecord(FlaskForm):
    artist_name = wt.StringField('Artist Name')
    album_name = wt.StringField('Album Name')
    genre = wt.StringField('Genre')
    play_count = wt5.IntegerField('Play Count')
    last_played = wt5.DateField('Last Played', format='%Y-%m-%d')
    ignore = wt5.IntegerField('Ignore?')
    release_type = wt.StringField('Release Type')
    sort_order = wt5.IntegerField('Sort Order')
    submit = wt.SubmitField('Update')



class AddRecord(FlaskForm):
    artist_name = wt.StringField('Artist Name')
    album_name = wt.StringField('Album Name')
    genre = wt.StringField('Genre')
    ignore = wt5.IntegerField('Ignore?')
    release_type = wt.StringField('Release Type')
    submit = wt.SubmitField('Update')



class BulkUpdate(FlaskForm):
	artist_name = wt.StringField('Artist Name')
	genre = wt.StringField('Genre')
	release_type = wt.StringField('Release Type')
	submit = wt.SubmitField('Update')



class Filters(FlaskForm):
    column_name = wt.SelectField(u'Column 1', choices=['Artist Name','Album Name','Genre','Release Type','Play Count','Last Played','Date Added','ID','Ignore'])
    row_value = wt.StringField('Row Value 1')
    column_name_2 = wt.SelectField('Column 2', choices=['','Artist Name','Album Name','Genre','Release Type','Play Count','Last Played','Date Added','ID','Ignore'])
    row_value_2 = wt.StringField('Row Value 2')
    submit = wt.SubmitField('Submit')



class RecommendGenre(FlaskForm):
    choice = wt.SelectField()
    submit = wt.SubmitField()


