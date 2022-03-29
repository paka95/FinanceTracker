from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from website.forms import ExpenseForm
from website.models import Expense
from website import db
from datetime import datetime, date
from sqlalchemy.sql import func, and_
from sqlalchemy import desc
from sqlalchemy import extract  


views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    now = datetime.now()
    now_formatted = now.strftime("%Y-%m-%d")
    return redirect(url_for('views.homedate', data = now_formatted))
    # form = ExpenseForm()
    # start = date(year=2022, month=3, day=26)
    # terazdata = date.today()

    # expenses = Expense.query.filter(func.date(Expense.date_created) == terazdata).order_by(desc(Expense.date_created)).all()
    # monthly_expenses = Expense.query.filter(func.date(Expense.date_created) == start).all()

    # total_expenses0 = 0
    # for expense in expenses:
    #     total_expenses0 = total_expenses0 + expense.amount
    #     total_expenses = round(total_expenses0, 2)
    # monthly_expenses = 0
    # if request.method == "POST":
    #     data = request.form.get('datah')
    #     if data:
    #         return redirect(url_for('views.homedate', data = data))
    #     if form.validate_on_submit():
    #         new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id)
    #         datah = request.form.get("datah")
    #         terazdata = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    #         db.session.add(new_expense)
    #         db.session.commit()
    #         return redirect(url_for('views.home'))

    # return render_template("home.html", form = form, expenses = expenses, total_expenses = total_expenses, terazdata=terazdata, monthly_expenses = monthly_expenses)


@views.route('/test', methods=['POST', 'GET'])
def test():
    form = ExpenseForm()
    expenses = Expense.query.filter_by(user_id = current_user.id).all()
    total_expenses0 = 0
    for expense in expenses:
        total_expenses0 = total_expenses0 + expense.amount
        total_expenses = round(total_expenses0, 2)
    if request.method == "POST":
        
        data = request.form.get('datah')
        return redirect(url_for('views.homedate', data = data))
    return render_template('test.html', form = form, expenses = expenses, total_expenses = total_expenses)




@views.route("/date/<data>", methods=['GET', 'POST'])
@login_required
def homedate(data):
    now = datetime.now()
    month_number = now.strftime("%m")
    month_number = int(month_number)

    form = ExpenseForm()
    expenses = Expense.query.filter(func.date(Expense.date_created) == data).filter(Expense.user_id == current_user.id).order_by(desc(Expense.date_created)).all()
    month = Expense.query.filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==month_number).all()
    # month = Expense.query.filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==4).all()
    

    montly_expenses = 0
    if month:
        for m in month:
            montly_expenses = montly_expenses + m.amount
            montly_rounded = round(montly_expenses, 2)
    else:
        montly_rounded = 0

    total_expenses0 = 0
    if expenses:
        for expense in expenses:
            total_expenses0 = total_expenses0 + expense.amount
            total_expenses = round(total_expenses0, 2)
    else:
        total_expenses = 0


    if request.method == "POST":
        lol = request.form.get('datah')
        print("lol:", lol)

        
        formatted = now.strftime("%Y-%m-%d")
        print("dzis data formatted:", formatted)
        if form.validate_on_submit():
            print("foremka1")
            lol2 = request.form.get('datah2')
            loldata = date(year=int(lol2[0:4]), month=int(lol2[5:7]), day=int(lol2[8:10]))
            formatted2 = date(year=int(formatted[0:4]), month=int(formatted[5:7]), day=int(formatted[8:10]))
            print("loldata:", loldata)
            print("type loldata:", type(loldata))
            print("formatted:", formatted)
            print("type formatted:", type(formatted))
            print("formatted:", formatted2)
            print("type formatted:", type(formatted2))
            if loldata == formatted2:
                print("loldata == sprawdz")
                new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id)
            else:
                print("else")
                new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id, date_created = data)
            db.session.add(new_expense)
            db.session.commit()
            return redirect(url_for('views.homedate', data = lol2))
        elif lol:
            print("foremka2")
            return redirect(url_for('views.homedate', data = lol))

    return render_template("home.html", form = form, expenses = expenses, terazdata = data, total_expenses = total_expenses, montly_rounded = montly_rounded)

