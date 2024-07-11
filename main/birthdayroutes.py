from flask import Blueprint, render_template, url_for, flash, request, redirect
from flask_login import current_user, login_required
from models.models import Birthdays
from main.forms import EditBirthdayForm
from models.transactions import get_by_birthday_id, birthday_record_exists, add, put, delete, DatabaseError, \
    IntegrityError
from extensions import limiter
from utils import sanitize_input, validate_email, validate_date
from datetime import datetime


birthdays_bp = Blueprint('birthdays', __name__)


@birthdays_bp.route('/save', methods=['GET', 'POST'])
@login_required
@limiter.limit("50 per hour")
def save():
    form = EditBirthdayForm()

    if request.method == 'POST':

        if not current_user.is_authenticated:
            flash("You need to log in to add birthdays.", "error")
            return redirect(url_for("auth.login"))

        email = request.form.get('email').lower().strip()
        name = sanitize_input(request.form.get('name')),
        date_str = request.form.get('date')

        if not all([name, email, date_str]):
            flash("Please fill all required fields", 'error')
            return redirect(url_for("birthdays.save"))

        is_valid_date, date_message = validate_date(date_str)
        if not is_valid_date:
            flash(date_message, 'error')
            return redirect(url_for('birthdays.save'))

        if not validate_email(email):
            flash('Invalid email format.', "error")
            return redirect(url_for("birthdays.save"))

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            new_birthday = Birthdays(
                author=current_user,
                name=name,
                date=date_obj,
                email=email
            )
            add(new_birthday)
            flash("Birthday record submitted successfully.", "success")

        except IntegrityError:
            flash('Birthday record already exists.', 'error')
            return redirect(url_for('auth.login'))

        except DatabaseError as e:
            flash(e.message, 'error')

        finally:
            return redirect(url_for('main.user'))

    return render_template('add.html', form=form)


@birthdays_bp.route("/edit-birthday/<int:birthday_id>", methods=["GET", "POST"])
@login_required
@limiter.limit("25 per hour")
def edit_birthday(birthday_id):
    try:
        birthday = get_by_birthday_id(Birthdays, birthday_id, current_user.id)

        if not birthday:
            flash('Birthday record not found', 'error')
            return redirect(url_for('main.user'))

        form = EditBirthdayForm(
            name=birthday.name,
            date=birthday.date,
            email=birthday.email
        )

        if form.submit.data and form.validate_on_submit():

            is_valid_date, date_message = validate_date(str(form.date.data))
            if not is_valid_date:
                flash(date_message, 'error')
                return redirect(url_for("birthdays.edit_birthday", birthday_id=birthday_id))

            email = form.email.data.lower().strip()
            if not validate_email(email):
                flash('Invalid email format.', "error")
                return redirect(url_for("birthdays.edit_birthday", birthday_id=birthday_id))

            birthday.name = sanitize_input(form.name.data)
            birthday.date = form.date.data
            birthday.email = email

            put()

            flash('Birthday record modified.', 'success')
            return redirect(url_for('main.user'))

        return render_template('edit.html', form=form)

    except DatabaseError as e:
        flash(e.message, 'error')

    return redirect(url_for("birthdays.edit_birthday", birthday_id=birthday_id))


@birthdays_bp.route("/delete/<int:birthday_id>", methods=["POST"])
@login_required
def delete_birthday(birthday_id):
    try:
        birthday_record = birthday_record_exists(Birthdays, birthday_id)

        if not birthday_record:
            flash("Birthday record not found", "error")
            return redirect(url_for("main.user"))

        birthday = get_by_birthday_id(Birthdays, birthday_id, current_user.id)

        if not birthday:
            flash("You are not allowed to delete this birthday record!", "error")
            return redirect(url_for("main.user"))

        delete(birthday)
        flash("Birthday record deleted successfully", "success")

    except DatabaseError as e:
        flash(e.message, 'error')

    finally:
        return redirect(url_for('main.user'))
