from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from website.forms import ExpenseForm
from website.models import Expense, User
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



@views.route("/<data>", methods=['GET', 'POST'])
@login_required
def homedate(data):
    now = datetime.strptime(data, "%Y-%m-%d")
    month_number = now.strftime("%m")
    month_number = int(month_number)

    form = ExpenseForm()
    user = User.query.filter_by(id=current_user.id).first()
    expenses = Expense.query.filter(func.date(Expense.date_created) == data).filter(Expense.user_id == current_user.id).order_by(desc(Expense.date_created)).all()
    month = Expense.query.filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==month_number).all()
    month_grouped = db.session.query(Expense.label, db.func.round(db.func.sum(Expense.amount), 2)).filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==month_number).group_by(Expense.label).all()

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
        else:
            lol2 = request.form.get('chosen_data_in_form')
            flash("Please enter smaller amount", category='danger')
            return redirect(url_for('views.homedate', data = lol2))

    return render_template("home.html", form = form, expenses = expenses, terazdata = data, total_expenses = total_expenses, montly_rounded = montly_rounded, user = user, month_grouped = month_grouped)



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
        print("name", first)
        print("label", second)
        print("amount", third)
        expense.name = first
        if second == None:
            expense.label = expense.label
            print("if", expense.label)
        else:
            expense.label = second
            print("else", expense.label)
        if float(third) > 99999:
            flash("Enter smaller amount", category='danger')
            return redirect(url_for("views.homedate", data = lol2))
        else:
            expense.amount = third
        flash("Expense updated", category='success')
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



@views.route("/preview/<dada>", methods=['GET', 'POST'])
@login_required
def preview(dada):
    month = int(dada[5:7])
    print("przeslana data", dada)
    user = User.query.filter_by(id=current_user.id).first()
    expenses = Expense.query.filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==month).order_by(desc(Expense.date_created)).all()

    monthly_expenses = 0
    if expenses:
        for m in expenses:
            monthly_expenses = monthly_expenses + m.amount
            monthly_rounded = round(monthly_expenses, 2)
    else:
        monthly_rounded = 0

    if request.method == 'POST':
        datt = request.form.get("datt")
        return redirect(url_for("views.preview", dada = datt))
    
    return render_template("preview.html", expenses = expenses, dada = dada[:7], monthly_rounded = monthly_rounded, dada_back = dada, user = user)



@views.route("/preview/<dada>/group", methods=['GET', 'POST'])
@login_required
def preview_grouped(dada):
    month_date = int(dada[5:7])
    print("dada:", dada)
    print("month_date:", month_date)
    user = User.query.filter_by(id=current_user.id).first()
    month = db.session.query(Expense.label, db.func.round(db.func.sum(Expense.amount), 2)).filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==month_date).group_by(Expense.label).all()

    total = 0
    for row in month:
        total = total + row[1]
    print(total)
    
    if request.method == 'POST':
        datt = request.form.get("datt")
        return redirect(url_for("views.preview_grouped", dada = datt))

    return render_template('preview_grouped.html', total = total, month = month, dada = dada, user = user)



@views.route("/change_currency", methods=['POST', 'GET'])
@login_required
def change_currency():
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == "POST":
        currency = request.form.get("cur")
        user.currency = currency
        db.session.commit()
    return redirect(url_for("views.profile"))



@views.route("/profile")
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    currency = user.currency
    return render_template("profile.html", user = user, currency = currency)



@views.route('/test', methods=['POST', 'GET'])
def test():
    return render_template('test.html')