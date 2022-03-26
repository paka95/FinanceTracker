from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from website.forms import ExpenseForm
from website.models import Expense
from website import db
from datetime import datetime, date
from sqlalchemy.sql import func, and_


views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    form = ExpenseForm()
    start = datetime(year=2022, month=3, day=26)
    end = datetime(year=2022, month=3, day=27)
    # expenses = Expense.query.filter_by(date_created = '2022-03-25 21:11:57', user_id = current_user.id).all()
    expenses = Expense.query.filter((Expense.date_created > start) & (Expense.date_created < end)).filter_by(user_id = 1).all()
    # expenses = Expense.query.filter_by(user_id = current_user.id).all()
    # datah = request.form.get("datah") # 2022-03-25
    terazczas = datetime.today()
    terazdata = date.today()
    print("type of expense: ", type(expenses[0].date_created))
    print("date created z db", expenses[0].date_created)
    print()
    print("type of terazczas: ", type(terazczas))
    print("terazczas", terazczas)
    print("terazczas", terazczas.strftime('%Y-%m-%d %H:%M:%S'))
    print()
    print("typ terazdata", type(terazdata))
    print(terazdata)
    print()
    print(start)
    print()
    print(type(start))
    # search_created = datetime.strptime('2022-03-25 21:11:57', '%Y-%m-%d %H:%M:%S')
    # print(type(search_created))

    # print(expenses)
    # print(expenses[1].date_created)
    total_expenses0 = 0
    for expense in expenses:
        total_expenses0 = total_expenses0 + expense.amount
        total_expenses = round(total_expenses0, 2)
    if request.method == "POST":
        if form.validate_on_submit():
            new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id)
            datah = request.form.get("datah")
            # datah = datetime.now()
            print(datah[5:10])
            db.session.add(new_expense)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("home.html", form = form, expenses = expenses, total_expenses = total_expenses)


@views.route('/test')
def test():
    form = ExpenseForm()
    expenses = Expense.query.filter_by(user_id = current_user.id).all()
    total_expenses0 = 0
    for expense in expenses:
        total_expenses0 = total_expenses0 + expense.amount
        total_expenses = round(total_expenses0, 2)
    return render_template('test.html', form = form, expenses = expenses, total_expenses = total_expenses)