from . import db

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Income {self.name}: {self.amount}>"

class Expenditure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Expenditure {self.name}: {self.amount}>"

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Goal {self.name or 'Goal'}: {self.value}>"