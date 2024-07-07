from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, ItemForm, BalanceForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market():
    
    purchase_form=PurchaseItemForm()
    sell_form=SellItemForm()
    if request.method == "POST":
        #Purchase items
        purchased_item=request.form.get('purchased_item')
        with app.app_context():
            p_item_object=Item.query.filter_by(name=purchased_item).first()
            if p_item_object:
                if current_user.can_purchase(p_item_object):
                    p_item_object.owner=current_user.id
                    current_user.budget -= p_item_object.price
                    db.session.commit()
                    flash(f"Congratulations !!! You purchased {p_item_object.name} for Rs. {p_item_object.price} successfully", category="success")
                else:
                    flash(f"Insufficient balance in your Account !!!", category="danger")
        #Sell items
        sell_item=request.form.get('sell_item')
        with app.app_context():
            s_item_object=Item.query.filter_by(name=sell_item).first()
            if s_item_object:
                if current_user.can_sell(s_item_object):
                    s_item_object.owner = None
                    current_user.budget += s_item_object.price
                    db.session.commit()
                    flash(f"{s_item_object.name} has been sold successfully for Rs. {s_item_object.price}", category="success")
                else:
                    flash(f"Sorry !!! Something went wrong !!! Please try again !!! ", category="danger")
        return redirect(url_for('market'))

    if request.method == "GET":
        with app.app_context():
            items=Item.query.filter_by(owner=None)
            owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)

@app.route('/register', methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        with app.app_context():
            user_data=User(username=form.username.data,
                           email_address=form.email_address.data,
                           password=form.password1.data)
            db.session.add(user_data)
            db.session.commit()
            login_user(user_data)
            flash(f'Account created successfully !!! You are now logged in as : {user_data.username}' , category='success')

        return redirect(url_for('market'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'You have successfully logged in as : {attempted_user.username}' , category='success')
            return redirect(url_for('market'))
        
        else:
            flash(f'Username and password do not match ! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out !!!", category='info')
    return redirect(url_for('home'))

@app.route('/add_items', methods=['GET','POST'])
def add_items():
    form=ItemForm()
    if form.validate_on_submit():
        with app.app_context():
            attempted_user = User.query.filter_by(username=current_user.username).first()
            if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                item_data=Item(name=form.item_name.data,
                            barcode=form.barcode.data,
                            price=form.item_price.data,
                            description=form.description.data,
                            owner=current_user.id)
                db.session.add(item_data)
                db.session.commit()
                flash(f'Item has been added to your Account successfully !!!', category='success')
                return redirect(url_for('market'))
            else:
                flash(f'Password does not match !!! Please try again !!! ', category='danger')  
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg[0]}', category='danger')          
    return render_template('items.html', form=form)
@app.route('/balance', methods=['GET', 'POST'])
def balance():
    form=BalanceForm()
    if form.validate_on_submit():
        with app.app_context():
            attempted_user=User.query.filter_by(username=form.username.data).first()
            if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                current_user.budget += form.amount.data
                db.session.commit()
                flash(f'Rs. {form.amount.data} has been added to your balance succesfully', category='success')
                return redirect(url_for('market'))
            else:
                flash(f'Username and password do not match ! Please try again', category='danger')
    return render_template('balance.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')