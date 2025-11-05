from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class IncomeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0.0)])
    submit = SubmitField("Add Income")

class ExpenditureForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0.0)])
    submit = SubmitField("Add Expenditure")

class GoalForm(FlaskForm):
    name = StringField("Name", validators=[Optional(), Length(max=120)])
    value = DecimalField("Goal Value", validators=[DataRequired(), NumberRange(min=0.0)])
    submit = SubmitField("Save Goal")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")

