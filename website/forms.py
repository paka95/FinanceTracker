from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

class RegisterForm(FlaskForm):
    email = StringField('EMAIL', validators=[DataRequired()])
    password = PasswordField('PASSWORD', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('CONFIRM PASSWORD', validators=[EqualTo('password')])
    submit = SubmitField('REGISTER')


class LoginForm(FlaskForm):
    email = StringField('EMAIL', validators=[DataRequired()])
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    submit = SubmitField('LOGIN')


class ExpenseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(max=99999, message='Enter smaller number')])
    labell = SelectField('Label', validators=[DataRequired()], choices=[('Select a label'), ('Transport'), ('Bills'), ('Food'), ('Misc'), ('Fees')])
    submit = SubmitField('Add expense')


