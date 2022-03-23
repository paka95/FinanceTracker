from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from website.forms import RegisterForm, LoginForm

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        flash('Logged in!', category='success')
        return redirect(url_for('views.home'))
    return render_template("login.html", form=form)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        flash('Register!', category='success')
        return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)