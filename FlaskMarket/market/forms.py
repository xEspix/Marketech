from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market import app
from market.models import User, Item



class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        with app.app_context():
            user=User.query.filter_by(username=username_to_check.data).first()

        if user:
            raise ValidationError('Username already exists! Please try a different username')
        
    def validate_email_address(self, email_address_to_check):
        with app.app_context():
            email=User.query.filter_by(email_address=email_address_to_check.data).first()

        if email:
            raise ValidationError('Email adress already exists! Please try a different email address')
        
    username = StringField(label='User Name :', validators=[Length(min=2, max=20), DataRequired()])
    email_address = StringField(label='Email Address : ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password : ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password : ', validators=[EqualTo('password2'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name : ', validators=[Length(min=2, max=20), DataRequired()])
    password = PasswordField(label='Password : ', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell')

class ItemForm(FlaskForm):
    def validate_barcode(self, barcode_to_check):
        with app.app_context():
            item=Item.query.filter_by(barcode=barcode_to_check.data).first()

        if item:
            raise ValidationError('Duplicate Barcode !!! Re-enter the correct Barcode')
        
    
    item_name = StringField(label='Item Name : ', validators=[Length(max=30), DataRequired()])
    barcode = IntegerField(label='Barcode : ', validators=[DataRequired()])
    item_price = FloatField(label='Price : ', validators=[DataRequired()])
    description = StringField(label='Description : ', validators=[Length(max=1024), DataRequired()])
    password = PasswordField(label='User Password : ', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Add this Item')
    
class BalanceForm(FlaskForm):
    username = StringField(label='User Name : ', validators=[Length(min=2, max=20), DataRequired()])
    password = PasswordField(label='Password : ', validators=[Length(min=6), DataRequired()])
    amount = FloatField(label='Add Amount : ', validators=[DataRequired()])
    submit = SubmitField(label="Confirm")