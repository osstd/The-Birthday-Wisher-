from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField("User Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("User Name", validators=[DataRequired()])
    submit = SubmitField("Register Me")


class LoginForm(FlaskForm):
    email = StringField("User Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class EditBirthdayForm(FlaskForm):
    name = StringField("User Name", validators=[DataRequired()])
    date = StringField("YYYY-MM-DD", validators=[DataRequired()])
    email = StringField("Recipient's Email", validators=[DataRequired()])
    submit = SubmitField("Submit")