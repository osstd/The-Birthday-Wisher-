from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from models.models import User
from models.transactions import get_all, get_user_by_id, delete, DatabaseError
from admin import admin_only

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('home.html')


@main_bp.route('/user')
@login_required
def user():
    if current_user.id != 1:
        return render_template('user.html', all_users=None)

    try:
        users = get_all(User)
        return render_template('user.html', all_users=users)
    except DatabaseError as e:
        flash(e.message, 'error')
        return render_template('user.html', all_users=None)


@main_bp.route("/delete-user/<int:user_id>")
@admin_only
@login_required
def delete_user(user_id):
    try:
        user_delete = get_user_by_id(User, user_id)

        if not user_delete:
            flash("User not found", "error")
            return redirect(url_for('main.user'))

        delete(user_delete)
        flash("User successfully deleted", "success")

    except DatabaseError as e:
        flash(e.message, 'error')

    finally:
        return redirect(url_for('main.user'))
