from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, login_user, current_user, logout_user
from website.forms import RegisterForm, LoginForm
from website import db, bcrypt
from website.models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Logged in {current_user.id}!', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Wrong credentials, try again', category='error')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Registered!', category='success')
        return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!', category='success')
    return redirect(url_for('auth.login'))