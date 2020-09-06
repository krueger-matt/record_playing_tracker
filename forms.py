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