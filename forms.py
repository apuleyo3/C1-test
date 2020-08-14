from flask_wtf import FlaskForm, validators
from wtforms import StringField, TextField, SubmitField, SelectField, IntegerField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length
from wtforms.validators import InputRequired, Email


class ContactForm(FlaskForm):
    firstname = StringField('Name', [DataRequired()])
    lastname = StringField('Lastname', [DataRequired()])
    email = StringField('Email', [Email(message=('Not a valid email address.')), DataRequired()])
    submit = SubmitField('Submit')

class QuestSel(FlaskForm):
    q_sel = RadioField('Select your answer', validators=[InputRequired()])

class QuestNum(FlaskForm):
    q_num = IntegerField('Select your aswer', [DataRequired()])

class QuestFeed(FlaskForm):
    q_feed = TextAreaField('Feedback')
