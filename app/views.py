from flask import render_template, redirect, url_for, request, flash, Blueprint
from . import db
from .models import Income, Expenditure, Goal
from .forms import IncomeForm, ExpenditureForm, GoalForm

bp = Blueprint("main", __name__)  # ✅ 蓝图

@bp.route("/")
def index():
    incomes = Income.query.all()
    expenditures = Expenditure.query.all()
    total_income = sum(i.amount for i in incomes)
    total_expenditure = sum(e.amount for e in expenditures)
    diff = total_income - total_expenditure
    goal = Goal.query.first()
    return render_template("index.html", incomes=incomes, expenditures=expenditures, diff=diff, goal=goal)

@bp.route("/income/add", methods=["GET", "POST"])
def add_income():
    form = IncomeForm()
    if form.validate_on_submit():
        item = Income(name=form.name.data or None, amount=float(form.amount.data))
        db.session.add(item)
        db.session.commit()
        flash("Income Added!")
        return redirect(url_for("main.index"))
    return render_template("add_income.html", form=form)

@bp.route("/expenditure/add", methods=["GET", "POST"])
def add_expenditure():
    form = ExpenditureForm()
    if form.validate_on_submit():
        item = Expenditure(name=form.name.data or None, amount=float(form.amount.data))
        db.session.add(item)
        db.session.commit()
        flash("Expenditure Added!")
        return redirect(url_for("main.index"))
    return render_template("add_expenditure.html", form=form)

@bp.route("/goal", methods=["GET", "POST"])
def goal():
    item = Goal.query.first()
    form = GoalForm(obj=item)
    if form.validate_on_submit():
        if not item:
            item = Goal()
            db.session.add(item)
        item.name = form.name.data or None
        item.value = float(form.value.data)
        db.session.commit()
        flash("Goal saved.")
        return redirect(url_for("main.goal"))
    return render_template("goal.html", form=form, item=item)

@bp.route("/goal/delete", methods=["POST"])
def delete_goal():
    item = Goal.query.first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Goal deleted.")
    return redirect(url_for("main.goal"))