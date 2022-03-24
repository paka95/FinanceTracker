from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from website.forms import ExpenseForm
from website.models import Expense
from website import db
from datetime import datetime


views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    form = ExpenseForm()
    expenses = Expense.query.filter_by(user_id = current_user.id).all()
    # print(type(expenses[1].date_created))
    total_expenses = 0
    for expense in expenses:
        total_expenses = total_expenses + expense.amount
    if request.method == "POST":
        if form.validate_on_submit():
            new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id)
            # datah = request.form.get("datah")
            # datah = datetime.now()
            # print(datah)
            db.session.add(new_expense)
            db.session.commit()
            return redirect(url_for('views.home'))



    return render_template("home.html", form = form, expenses = expenses, total_expenses = total_expenses)


@views.route('/test')
def test():
    return render_template('test.html')