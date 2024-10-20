from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Optional

class MemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Optional()])
    phone = StringField('Phone', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    join_date = DateField('Join Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class MembershipTypeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    term_value = IntegerField('Term Value (e.g., 1)', validators=[DataRequired()])
    term_interval = StringField('Term Interval (e.g., year, month)', validators=[DataRequired()])
    extension_value = IntegerField('Extension Value (e.g., 1)', validators=[DataRequired()])
    extension_interval = StringField('Extension Interval (e.g., year, month)', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    price_interval = StringField('Price Interval (e.g., year)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MembershipForm(FlaskForm):
    membership_type = SelectField('Membership Type', coerce=int, validators=[DataRequired()])
    membership_start = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    membership_end = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Assign Membership')
