from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EditBirthdayForm(FlaskForm):
    name = StringField("User Name", validators=[DataRequired()])
    date = StringField("YYYY-MM-DD", validators=[DataRequired()])
    email = StringField("Recipient's Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

