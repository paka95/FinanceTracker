from unicodedata import category
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


@views.route('/test', methods=['POST', 'GET'])
def test():
    return render_template('test.html')



# @views.route('/test2', methods=['POST', 'GET'])
# def test2():
#     form = ExpenseForm()
#     expenses = Expense.query.filter_by(user_id = current_user.id).all()
#     total_expenses0 = 0
#     for expense in expenses:
#         total_expenses0 = total_expenses0 + expense.amount
#         total_expenses = round(total_expenses0, 2)
#     if request.method == "POST":
        
#         data = request.form.get('datah')
#         return redirect(url_for('views.homedate', data = data))
#     return render_template('test2.html', form = form, expenses = expenses, total_expenses = total_expenses)


# @views.route('/test3', methods=['POST', 'GET'])
# def test3():
#     form = ExpenseForm()
#     expenses = Expense.query.filter_by(user_id = current_user.id).all()
#     total_expenses0 = 0
#     for expense in expenses:
#         total_expenses0 = total_expenses0 + expense.amount
#         total_expenses = round(total_expenses0, 2)
#     if request.method == "POST":
        
#         data = request.form.get('datah')
#         return redirect(url_for('views.homedate', data = data))
#     return render_template('test3.html', form = form, expenses = expenses, total_expenses = total_expenses)




@views.route("/<data>", methods=['GET', 'POST'])
@login_required
def homedate(data):
    # now = datetime.now()
    now = datetime.strptime(data, "%Y-%m-%d")
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
        chosen_data = request.form.get('chosen_data')
        month_specified = int(data[5:7])
        print("lol:", chosen_data)

        today = datetime.now()
        formatted = today.strftime("%Y-%m-%d")
        if form.validate_on_submit():
            lol2 = request.form.get('chosen_data_in_form')
            loldata = date(year=int(lol2[0:4]), month=int(lol2[5:7]), day=int(lol2[8:10]))
            formatted2 = date(year=int(formatted[0:4]), month=int(formatted[5:7]), day=int(formatted[8:10]))
            if loldata == formatted2:
                new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id)
            else:
                print("data dodania to:", data)
                new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id, date_created = data)
            db.session.add(new_expense)
            db.session.commit()
            flash("Expense added", category="success")
            return redirect(url_for('views.homedate', data = lol2))
        elif chosen_data:
            return redirect(url_for('views.homedate', data = chosen_data))

    return render_template("home.html", form = form, expenses = expenses, terazdata = data, total_expenses = total_expenses, montly_rounded = montly_rounded)


@views.route("/change_expense/<id>", methods=['GET', 'POST'])
@login_required
def change_expense(id):
    expense = Expense.query.filter_by(id = id).first()
    lol2 = request.form.get('chosen_data_in_form')

    if not expense:
        flash("No record found", category="danger")
    else:
        first = request.form.get("updatename")
        second = request.form.get("updatelabel")
        third = request.form.get("updateamount")
        if first and second and third:
            expense.name = first
            expense.label = second
            expense.amount = third
            flash("Whole expense updated", category="success")
        elif first and second:
            expense.name = first
            expense.label = second
            flash("Updated name and label", category="success")
        elif first and third:
            expense.name = first
            expense.amount = third
            flash("Updated name and amount", category="success")
        elif second and third:
            expense.label = second
            expense.amount = third
            flash("Updated label and amount", category="success")
        elif first:
            expense.name = first
            flash("Updated name", category="success")
        elif second:
            expense.label = second
            flash("Updated label", category="success")
        elif third:
            expense.amount = third
            flash("Updated amount", category="success")
        else:
            flash("Nothing updated", category="info")
        db.session.commit()
        return redirect(url_for("views.homedate", data = lol2))
    return render_template("home.html")



@views.route("/delete_expense/<id>", methods=['GET', 'POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    lol2 = request.form.get('chosen_data_in_form')

    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted", category="success")
    return redirect(url_for("views.homedate", data = lol2))