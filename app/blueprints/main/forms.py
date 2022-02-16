from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, EqualTo, ValidationError
from app.models import User

class PokeForm(FlaskForm):
    #field name = DataTypeField('LABEL', validators=[LIST OF validators])
    poke= StringField('What Pokemon would you like to search for?',validators = [DataRequired()])
    submit = SubmitField('Search')
