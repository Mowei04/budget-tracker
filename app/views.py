from flask import Blueprint, flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError

from . import db
from .forms import DeleteForm, ExpenditureForm, GoalForm, IncomeForm
from .models import Expenditure, Goal, Income

bp = Blueprint("main", __name__)  # ✅ 蓝图

@bp.route("/")
def index():
    incomes = Income.query.order_by(Income.id.desc()).all()
    expenditures = Expenditure.query.order_by(Expenditure.id.desc()).all()
    total_income = sum(i.amount for i in incomes)
    total_expenditure = sum(e.amount for e in expenditures)
    diff = total_income - total_expenditure
    goal = Goal.query.first()
    progress = None
    if goal and goal.value:
        try:
            progress = max(min((diff / goal.value) * 100, 100), 0)
        except ZeroDivisionError:
            progress = None
    return render_template(
        "index.html",
        incomes=incomes,
        expenditures=expenditures,
        total_income=total_income,
        total_expenditure=total_expenditure,
        diff=diff,
        goal=goal,
        progress=progress,
    )

@bp.route("/incomes", methods=["GET", "POST"])
def incomes():
    form = IncomeForm()
    if form.validate_on_submit():
        item = Income(name=form.name.data, amount=float(form.amount.data))
        db.session.add(item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Income with this name already exists.", "error")
        else:
            flash("Income added!")
        return redirect(url_for("main.incomes"))
    items = Income.query.order_by(Income.id.desc()).all()
    delete_forms = {item.id: DeleteForm(formdata=None) for item in items}
    return render_template("income_list.html", form=form, items=items, delete_forms=delete_forms)


@bp.route("/income/<int:item_id>/edit", methods=["GET", "POST"])
def edit_income(item_id):
    item = Income.query.get_or_404(item_id)
    form = IncomeForm(obj=item)
    form.submit.label.text = "Update Income"
    if form.validate_on_submit():
        item.name = form.name.data
        item.amount = float(form.amount.data)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Income with this name already exists.", "error")
        else:
            flash("Income updated.")
        return redirect(url_for("main.incomes"))
    return render_template("edit_income.html", form=form, item=item)


@bp.route("/income/<int:item_id>/delete", methods=["POST"])
def delete_income(item_id):
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "error")
        return redirect(url_for("main.incomes"))
    item = Income.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Income deleted.")
    return redirect(url_for("main.incomes"))

@bp.route("/expenditures", methods=["GET", "POST"])
def expenditures():
    form = ExpenditureForm()
    if form.validate_on_submit():
        item = Expenditure(name=form.name.data, amount=float(form.amount.data))
        db.session.add(item)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Expenditure with this name already exists.", "error")
        else:
            flash("Expenditure added!")
        return redirect(url_for("main.expenditures"))
    items = Expenditure.query.order_by(Expenditure.id.desc()).all()
    delete_forms = {item.id: DeleteForm(formdata=None) for item in items}
    return render_template("expenditure_list.html", form=form, items=items, delete_forms=delete_forms)


@bp.route("/expenditure/<int:item_id>/edit", methods=["GET", "POST"])
def edit_expenditure(item_id):
    item = Expenditure.query.get_or_404(item_id)
    form = ExpenditureForm(obj=item)
    form.submit.label.text = "Update Expenditure"
    if form.validate_on_submit():
        item.name = form.name.data
        item.amount = float(form.amount.data)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Expenditure with this name already exists.", "error")
        else:
            flash("Expenditure updated.")
        return redirect(url_for("main.expenditures"))
    return render_template("edit_expenditure.html", form=form, item=item)


@bp.route("/expenditure/<int:item_id>/delete", methods=["POST"])
def delete_expenditure(item_id):
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "error")
        return redirect(url_for("main.expenditures"))
    item = Expenditure.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Expenditure deleted.")
    return redirect(url_for("main.expenditures"))

@bp.route("/goal", methods=["GET", "POST"])
def goal():
    item = Goal.query.first()
    form = GoalForm(obj=item)
    delete_form = DeleteForm()
    if form.validate_on_submit():
        if not item:
            item = Goal()
            db.session.add(item)
        item.name = form.name.data or None
        item.value = float(form.value.data)
        db.session.commit()
        flash("Goal saved.")
        return redirect(url_for("main.goal"))
    return render_template("goal.html", form=form, item=item, delete_form=delete_form)

@bp.route("/goal/delete", methods=["POST"])
def delete_goal():
    form = DeleteForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "error")
        return redirect(url_for("main.goal"))
    item = Goal.query.first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Goal deleted.")
    return redirect(url_for("main.goal"))

