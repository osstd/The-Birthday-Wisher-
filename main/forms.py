from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, ValidationError
from utils import validate_date


class EditBirthdayForm(FlaskForm):
    name = StringField("User Name", validators=[DataRequired()])
    date = DateField("Birthday", format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField("Recipient's Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_date(self, field):
        is_valid, message = validate_date(field.data.strftime('%Y-%m-%d'))
        if not is_valid:
            raise ValidationError(message)
