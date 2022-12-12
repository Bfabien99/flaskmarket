from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskmarket.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    
    def __repr__(self) -> str:
        return f'Item {self.name}'
    
    
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Item {self.name}'
        
        
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,email_address=form.email_address.data,password_hash=form.password1.data,)
        
        try:
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('market_page'))
        except:
            db.session.rollback()
            if User.query.filter_by(username=form.username.data).first():
                flash("Username already exists! Please try a different username","danger")
                
            if User.query.filter_by(email_address=form.email_address.data).first():
                flash("Email already exists! Please try a different email","danger")
                
    if form.errors != {}: # If there are errors
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", "danger")
            
    return render_template('signup.html', form=form)
    
if __name__ == '__main__':
    app.run()