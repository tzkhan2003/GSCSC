from flask import render_template, url_for, flash, redirect, request, Blueprint, send_file
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Member, SellerId
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, Memberform)
from flaskblog.users.utils import save_picture, send_reset_email
import pandas as pd
import openpyxl

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Memberform()
    print(form)
    if form.validate_on_submit():
        #print(form.picture.data)
        picture_file = save_picture(form.picture.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usera = User(username=form.name.data, email=form.email.data, password=hashed_password,birth_date=form.birth_date.data,type='member')
        user = Member(token=form.token.data, name=form.name.data, email=form.email.data,passwordorg=form.password.data, password=hashed_password,birth_date=form.birth_date.data, father_name=form.father_name.data, father_ocu = form.father_ocu.data,
                        mother_name=form.mother_name.data, mother_ocu=form.mother_ocu.data, parents_no=form.parents_no.data, present_address=form.present_address.data, permanent_address=form.permanent_address.data, roll=form.roll.data, year = form.year.data, nid = form.nid.data,
                        phone=form.phone.data, facebook=form.facebook.data, picture=picture_file, exp= form.exp.data, school = form.school.data)
        db.session.add(user)
        db.session.add(usera)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.status == 'delete':
            return "<h1>Your account has been deleted</h1>"
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            print(picture_file)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>/post")
@login_required
def user_posts(username):
    if current_user.username == 'lampofcheer':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user,title='Post')



def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


@users.route('/database/<string:table>/export', methods=['GET', 'POST'])
@login_required
def exportexcel(table):
    if current_user.username == 'lampofcheer' or current_user.type == 'admin':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    if current_user.is_authenticated:
        if table == 'member':
            data = Member.query.all()
        if table == 'admin':
            data = SellerID.query.all()
        if table == 'user':
            data = User.query.all()
        data_list = [to_dict(item) for item in data]
        df = pd.DataFrame(data_list)
        filename = "data"+ table +".xlsx"
        print("Filename: "+filename)

        writer = pd.ExcelWriter(filename)
        df.to_excel(writer, sheet_name='Registrados')
        writer.save()

        return send_file(filename)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
