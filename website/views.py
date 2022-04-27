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
    todays_date = datetime.now()
    todays_date_formatted = todays_date.strftime("%Y-%m-%d")
    return redirect(url_for('views.homedate', expense_date = todays_date_formatted))



@views.route("/<expense_date>", methods=['GET', 'POST'])
@login_required
def homedate(expense_date):
    now = datetime.strptime(expense_date, "%Y-%m-%d")
    month_number = now.strftime("%m")
    month_number = int(month_number)

    form = ExpenseForm()
    user = User.query.filter_by(id=current_user.id).first()
    expenses = Expense.query.filter(func.date(Expense.date_created) == expense_date).filter(Expense.user_id == current_user.id).order_by(desc(Expense.date_created)).all()
    month = Expense.query.filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==month_number).all()
    month_grouped = db.session.query(Expense.label, db.func.round(db.func.sum(Expense.amount), 2)).filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==month_number).group_by(Expense.label).all()

    monthly_expenses = 0
    if month:
        for m in month:
            monthly_expenses = monthly_expenses + m.amount
            monthly_rounded = round(monthly_expenses, 2)
    else:
        monthly_rounded = 0
    
    total_expenses = 0
    if expenses:
        for expense in expenses:
            total_expenses = total_expenses + expense.amount
            total_expenses_rounded = round(total_expenses, 2)
    else:
        total_expenses_rounded = 0


    if request.method == "POST":
        date_picker_date = request.form.get('date_picker_date') #value of changed date when changing dates
        # month_specified = int(expense_date[5:7])
        # print("date_picker_date:", date_picker_date)

        today_datetime = datetime.now()
        today_formatted = today_datetime.strftime("%Y-%m-%d")

        if form.validate_on_submit():
            specified_date = request.form.get('date_picker_date_in_form')
            specified_expense_date = date(year=int(specified_date[0:4]), month=int(specified_date[5:7]), day=int(specified_date[8:10]))
            # print("specified_expense_date: ", specified_expense_date)
            today_formatted = date(year=int(today_formatted[0:4]), month=int(today_formatted[5:7]), day=int(today_formatted[8:10]))
            if specified_expense_date == today_formatted:
                new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id)
                # print("specified_expense_date2: ", specified_expense_date)
            else:
                # print("expense_date to:", expense_date)
                # print("specified_expense_date3: ", specified_expense_date)
                new_expense = Expense(name = form.name.data, amount = form.amount.data, label = form.labell.data, user_id = current_user.id, date_created = expense_date)
            db.session.add(new_expense)
            db.session.commit()
            flash("Expense added", category="success")
            return redirect(url_for('views.homedate', expense_date = specified_date))
        elif date_picker_date:
            return redirect(url_for('views.homedate', expense_date = date_picker_date))
        else:
            specified_date = request.form.get('date_picker_date_in_form')
            flash("Please enter smaller amount", category='danger')
            return redirect(url_for('views.homedate', expense_date = specified_date))

    return render_template("home.html", form = form, expenses = expenses, terazdata = expense_date, total_expenses = total_expenses_rounded, monthly_rounded = monthly_rounded, user = user, month_grouped = month_grouped)



@views.route("/change_expense/<id>", methods=['GET', 'POST'])
@login_required
def change_expense(id):
    expense = Expense.query.filter_by(id = id).first()
    specified_date = request.form.get('date_picker_date_in_form')

    if not expense:
        flash("No record found", category="danger")
    else:
        first = request.form.get("updatename")
        second = request.form.get("updatelabel")
        third = request.form.get("updateamount")
        expense.name = first
        if second == None:
            expense.label = expense.label
        else:
            expense.label = second
        if float(third) > 99999:
            flash("Enter smaller amount", category='danger')
            return redirect(url_for("views.homedate", expense_date = specified_date))
        else:
            expense.amount = third
        flash("Expense updated", category='success')
        db.session.commit()
        return redirect(url_for("views.homedate", expense_date = specified_date))
    return render_template("home.html")



@views.route("/delete_expense/<id>", methods=['GET', 'POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    specified_date = request.form.get('date_picker_date_in_form')

    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted", category="success")
    return redirect(url_for("views.homedate", expense_date = specified_date))



@views.route("/preview/<expense_month>", methods=['GET', 'POST'])
@login_required
def preview(expense_month):
    month = int(expense_month[5:7])
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
        return redirect(url_for("views.preview", expense_month = datt))
    
    return render_template("preview.html", expenses = expenses, expense_month = expense_month[:7], monthly_rounded = monthly_rounded, user = user)



@views.route("/preview/<expense_month>/group", methods=['GET', 'POST'])
@login_required
def preview_grouped(expense_month):
    month_date = int(expense_month[5:7])
    user = User.query.filter_by(id=current_user.id).first()
    month = db.session.query(Expense.label, db.func.round(db.func.sum(Expense.amount), 2)).filter_by(user_id = current_user.id).filter(extract('month', Expense.date_created)==month_date).group_by(Expense.label).all()

    total = 0
    for row in month:
        total = total + row[1]
    
    if request.method == 'POST':
        datt = request.form.get("datt")
        return redirect(url_for("views.preview_grouped", expense_month = datt))

    return render_template('preview_grouped.html', total = total, month = month, expense_month = expense_month, user = user)



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
    return render_template("profile.html", user = user)



@views.route('/test', methods=['POST', 'GET'])
def test():
    return render_template('test.html')


