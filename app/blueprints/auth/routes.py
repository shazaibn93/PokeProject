from . import bp as auth
from .forms import LoginForm, RegisterForm, EditProfileForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask import Flask, render_template, request, flash, redirect, url_for
import requests

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        #We will do the login stuff here
        email = request.form.get('email').lower()
        password = request.form.get('password')
        U = User.query.filter_by(email=email).first() #Left is column, right is variable
        if U and U.check_hashed_password(password):
            login_user(U)
            flash('Welcome to Fakebook', 'success')
            return redirect(url_for('auth.login'))
        flash("Incorrect Email Password Combo")
        return render_template('login.html.j2', form = form)
    return render_template('login.html.j2', form = form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('auth.login'))



@auth.route('/register',methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        #Create a new user 
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            #creating an empty user 
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            flash("We ran into an error ",'danger')
            #Error Return
            return render_template('register.html.j2', form=form)
        # If it worked
        flash('You have successfully registered', 'success')
        return redirect(url_for('auth.login'))
    #Get Return
    return render_template('register.html.j2', form=form)

@auth.route('/editprofile', methods= ['GET', 'POST'])
@login_required
def editprofile():
    form = EditProfileForm
    if request.method == 'Post' and form.validate_on_submit():
        new_user_data = {
            "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
        }
        user = User.query.filter_by(email = form.email.data.lower()).first()
        if user and user.email != current_user.email:
            flash('Email already in use','danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated', 'success')
        except:
            flash('Something went wrong. Surprisingly, not your fault','danger')
            return redirect(url_for('auth.edit_profile'))
        return redirect(url_for('main.index'))
    return render_template('register.html.j2', form=form)