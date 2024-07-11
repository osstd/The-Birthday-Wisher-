from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp


class RegisterForm(FlaskForm):
    email = StringField("User Email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'(?=.*[A-Z])', message="Must contain at least one uppercase letter"),
        Regexp(r'(?=.*[a-z])', message="Must contain at least one lowercase letter"),
        Regexp(r'(?=.*\d)', message="Must contain at least one digit"),
        Regexp(r'(?=.*[@$!%*?&])', message="Must contain at least one special character")
    ], render_kw={"id": "passwordField"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    name = StringField("User Name", validators=[DataRequired()])
    submit = SubmitField("Register Me")


class LoginForm(FlaskForm):
    email = StringField("User Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")
