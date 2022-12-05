from flask import render_template, request, Blueprint, flash, redirect, url_for,session
from flaskblog.models import SellerId, User, Member
from flaskblog.main.forms import Contact, Sellerform
from flaskblog import db, bcrypt
from flask import request,make_response
import requests
from flaskblog.users.utils import get_country ,call_api
from flask_login import current_user, login_required
from flaskblog.users.utils import save_pro_picture ,send_email
import secrets
import json
import pdfkit
import stripe

config=pdfkit.configuration(wkhtmltopdf=r'.\flaskblog\bin\wkhtmltopdf.exe')
buplishable_key ='pk_test_51IJhisCvsB7CERUXznrhAbCUHPmY1WDcqwnseIFRVLWiQHs49EgchoODlorCmpCkYnKOx4CtyPOJeNTEx7ksU8bS00Am5A3LR4'
stripe.api_key ='sk_test_51IJhisCvsB7CERUX2Gq7tiMiSMT2VecnDuc5mlfPp3bbGaWHGpfmbTgJ6OimECeEQ1C8Tw2HD84q5iNS1JZKSkMr00iXJwgdXx'

main = Blueprint('main', __name__)


@main.route("/")
def index():

	return render_template('index.html')


@main.route("/about")
def about():
	form = Contact()
	if form.validate_on_submit():
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.index'))

	return render_template('about.html', title='About' , form=form)



@main.route("/panel/registration", methods=['GET', 'POST'])
def sellerreg():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	else:
		form = Sellerform()
		if form.validate_on_submit():
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = User(username=form.username.data, email=form.email.data, password=hashed_password,birth_date=form.birth_date.data,type='panel')
			sellid=SellerId(username=form.username.data, email=form.email.data, birth_date=form.birth_date.data,password=form.password.data,trade=form.Parents_No.data,nid=form.nid.data,phone=form.phone.data,address=form.address.data,shopname=form.panel.data)
			db.session.add(sellid)
			db.session.add(user)
			db.session.commit()
			res = User.query.filter_by(type='admin')
			body = 'panel name: '+form.username.data +form.username.data+ " email " +form.email.data+ ' birth date '+ form.birth_date.data + ' hashed_password ' + str(hashed_password) + 'additional no '+ form.Parents_No.data + ' NID ' +form.nid.data+ ' Phone No ' +form.phone.data+ ' address ' +form.address.data+ ' panel ' + form.panel.data
			send_email(res,'New Panel added',body)
			return redirect(url_for('main.index'))
	return render_template('seller.html', title='Panel registration',form=form)



@main.route('/dashboard/account/<int:id>/delete', methods=['GET','POST'])
@login_required
def admin_account_delete(id):
	if current_user.username == 'lampofcheer' or current_user.type == 'admin':
		a = 1
	elif current_user.status != 'approve':
		return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
	if current_user.is_authenticated:
		if current_user.type == 'admin' or current_user.username == 'lampofcheer':
			post=User.query.filter_by(id=id).first()
			membership = Member.query.filter_by(name=post.username).first()
			membership.status = 'delete'
			post.status = 'delete'
			db.session.commit()
			res = User.query.filter_by(type='admin')
			body = post.username +','+post.email+" by " + current_user.email + ' , ' + current_user.username
			send_email(res,'account deleted',body)
			flash('Your post has been deleted!', 'success')
			return redirect(url_for('main.dashboard_account_pending'))

	else:
			return "<h3>Admin Login Required.</h3>"


@main.route('/dashboard/account/<int:id>/approve', methods=['GET','POST'])
@login_required
def admin_account_approve(id):
	if current_user.username == 'lampofcheer' or current_user.type == 'admin':
		a = 1
	elif current_user.status != 'approve':
		return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
	if current_user.is_authenticated:
		if current_user.type == 'admin' or current_user.username == 'lampofcheer':
			post=User.query.filter_by(id=id).first()
			post.status = 'approve'
			if post.type == 'member':
				membership = Member.query.filter_by(name=post.username).first()
				membership.status = 'approve'
				membership.memberid = str(membership.year) + str(membership.roll) + str(membership.id)
			db.session.commit()
			res = User.query.filter_by(type='admin')
			body = post.username +','+post.email+" by " + current_user.email + ' , ' + current_user.username
			#send_email(res,'account approved',body)
			flash('Your post has been approved!', 'success')
			return redirect(url_for('main.dashboard_account_pending'))

	else:
			return "<h3>Admin Login Required.</h3>"


@main.route('/dashboard/account/<int:id>/pending', methods=['GET','POST'])
@login_required
def admin_account_pending(id):
	if current_user.username == 'lampofcheer' or current_user.type == 'admin':
		a = 1
	elif current_user.status != 'approve':
		return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
	if current_user.is_authenticated:
		if current_user.type == 'admin' or current_user.username == 'lampofcheer':
			post=User.query.filter_by(id=id).first()
			post.status = 'pending'
			membership = Member.query.filter_by(name=post.username).first()
			membership.status = 'pending'
			db.session.commit()
			res = User.query.filter_by(type='admin')
			body = postusername +','+post.email+" by " + current_user.email + ' , ' + current_user.username
			send_email(res,'account freezed',body)
			flash('Your post has been approved!', 'success')
			return redirect(url_for('main.dashboard_account_approve'))

	else:
			return "<h3>Admin Login Required.</h3>"






@main.route('/thanks')
def thanks():
    return render_template('thank.html')




@main.route('/dashboard/account/pending', methods=['GET','POST'])
@login_required
def dashboard_account_pending():
	if current_user.username == 'lampofcheer' or current_user.type == 'admin':
		a = 1
	elif current_user.status != 'approve':
		return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
	post = User.query.filter_by(status='pending').all()
	return render_template('dashboard_account_pending.html', title='dashboard' , posts = post)


@main.route('/dashboard/account/approved', methods=['GET','POST'])
@login_required
def dashboard_account_approve():
	if current_user.username == 'lampofcheer' or current_user.type == 'admin':
		a = 1
	elif current_user.status != 'approve':
		return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
	post = User.query.filter_by(status='approve').all()
	return render_template('dashboard_account_approve.html', title='dashboard' , posts = post)



@main.route('/dashboard/account/delete', methods=['GET','POST'])
@login_required
def dashboard_account_delete():
	if current_user.username == 'lampofcheer' or current_user.type == 'admin':
		a = 1
	elif current_user.status != 'approve':
		return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
	post = User.query.filter_by(status='delete').all()
	return render_template('dashboard_account_delete.html', title='dashboard' , posts = post)






@main.route('/dashboard/account/<int:id>/admin', methods=['GET','POST'])
@login_required
def admin_account_admin(id):
	if current_user.username == 'lampofcheer' or current_user.type == 'admin':
		a = 1
	elif current_user.status != 'approve':
		return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
	if current_user.is_authenticated:
		if current_user.type == 'admin' or current_user.username == 'lampofcheer':
			post=User.query.filter_by(id=id).first()
			post.type = 'admin'
			db.session.commit()
			res = User.query.filter_by(type='admin')
			body = post.username +','+post.email+" by " + current_user.email + ' , ' + current_user.username
			send_email(res,'admin added',body)
			flash('Your post has been approved!', 'success')
			return redirect(url_for('main.dashboard_account_approve'))

	else:
			return "<h3>Admin Login Required.</h3>"


'''@main.route('/dashboard/account/<int:id>/panel', methods=['GET','POST'])
@login_required
def admin_account_panel(id):
	if current_user.username == 'lampofcheer' or current_user.type == 'admin':
		a = 1
	elif current_user.status != 'approve':
		return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
	if current_user.is_authenticated:
		if current_user.type == 'admin' or current_user.username == 'lampofcheer':
			brands = Brandname.query.all()
			categories = Catagoryname.query.all()
			post=User.query.filter_by(id=id).first()
			post.type = 'panel'
			db.session.commit()
			res = User.query.filter_by(type='admin')
			body = post.username +','+post.email+" by " + current_user.email + ' , ' + current_user.username
			send_email(res,'panel added',body)
			flash('Your post has been approved!', 'success')
			return redirect(url_for('main.dashboard_account_approve'))

	else:
			return "<h3>Admin Login Required.</h3>"'''






