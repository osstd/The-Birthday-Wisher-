from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from forms import RegisterForm, LoginForm, EditBirthdayForm
import os


# Wrapper if id is not 1 then return abort with 403 error
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('F_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///birthdays.db")
db = SQLAlchemy()
db.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    birthdays = relationship("Birthdays", back_populates="author", cascade="all, delete-orphan")


class Birthdays(db.Model):
    __tablename__ = "birthdays"
    id = db.Column(db.Integer, primary_key=True)
    # Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Create reference to the User object, the "birthday" refers to the birthdays property in the User class.
    author = relationship("User", back_populates="birthdays")
    name = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('home.html', logged_in=current_user.is_authenticated)


@app.route('/add')
@login_required
def add():
    return render_template('add.html', logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))
        if result.scalar():
            flash('Email already registered, login with email instead!')
            return redirect(url_for('login'))
        else:
            hash_and_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=email,
                name=request.form.get('name'),
                password=hash_and_salted_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("Email not found!")
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('index'))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index', logged_in=False))


@app.route('/save', methods=['POST'])
@login_required
def save():
    if request.method == 'POST':
        name = request.form['name']
        date_ = request.form['date']
        email = request.form['email']
        new_birthday = Birthdays(
            author=current_user,
            name=name,
            date=date_,
            email=email
        )
        db.session.add(new_birthday)
        db.session.commit()
        return render_template('add.html', logged_in=current_user.is_authenticated)


@app.route("/edit-birthday/<int:birthday_id>", methods=["GET", "POST"])
@login_required
def edit_birthday(birthday_id):
    birthday = db.get_or_404(Birthdays, birthday_id)
    edit_form = EditBirthdayForm(
        name=birthday.name,
        date=birthday.date,
        email=birthday.email
    )
    if edit_form.validate_on_submit():
        birthday.name = edit_form.name.data
        birthday.date = edit_form.date.data
        birthday.email = edit_form.email.data
        db.session.commit()
        return redirect(url_for('user'))
    return render_template('edit.html', form=edit_form, logged_in=current_user.is_authenticated)


@app.route("/delete/<int:birthday_id>")
@login_required
def delete_birthday(birthday_id):
    birthday_ids = [birthday.id for birthday in current_user.birthdays]
    if birthday_id in birthday_ids:
        birthday_to_delete = db.get_or_404(Birthdays, birthday_id)
        db.session.delete(birthday_to_delete)
        db.session.commit()
        return redirect(url_for('user'))
    flash('You are not allowed to delete this birthday record!')
    return redirect(url_for('user'))


@app.route("/delete-user/<int:user_id>")
@admin_only
@login_required
def delete_user(user_id):
    user_to_delete = db.session.get(User, user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
    return redirect(url_for('user'))


@app.route('/user')
@login_required
def user():
    if current_user.id == 1:
        records = db.session.execute(db.select(User))
        users = records.scalars().all()
        all_users = users
    else:
        all_users = None
    return render_template('user.html', user=current_user, all_users=all_users, logged_in=current_user.is_authenticated)


if __name__ == '__main__':
    app.run(debug=False)
