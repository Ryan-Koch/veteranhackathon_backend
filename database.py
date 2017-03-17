from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import and_
from flask import Flask
import datetime
import hashlib
from app import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vetbenefits.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class veterans(db.Model):
	id = db.Column('veteran_id', db.Integer, primary_key = True)
	first_name = db.Column('first_name', db.String(100))
	last_name = db.Column('last_name', db.String(100))
	address_1 = db.Column('address_1', db.String(200))
	address_2 = db.Column('address_2', db.String(200))
	city = db.Column('city', db.String(100))
	state = db.Column('state', db.String(100))
	zip_code = db.Column('zip_code', db.Integer)
	serve = db.Column('serve', db.Boolean)
	branch = db.Column('branch', db.String(20))
	active_duty = db.Column('active_duty', db.Boolean)
	pre_1980 = db.Column('pre_1980', db.Boolean)
	discharge_char = db.Column('discharge_char', db.String(50))
	injuries = db.Column('injuries', db.String(100))
	rec_treatment = db.Column('rec_treatment', db.Boolean)
	injuries_persist = db.Column('injuries_persist', db.Boolean)
	mental_h_need = db.Column('mental_h_need', db.Boolean)
	mental_h_issues = db.Column('mental_h_issues', db.String(100))
	sexual_assault = db.Column('sexual_assault', db.Boolean)
	combat_zone = db.Column('combat_zone', db.Boolean)
	filed_prev = db.Column('filed_prev', db.Boolean)
	eligible = db.Column('eligible', db.Boolean)
	email = db.Column('email', db.String(100), unique=True)
	password = db.Column('password', db.String(200))

	def __init__(self, 
			first_name, 
			last_name, 
			address_1,
			address_2,
			city,
			state,
			zip_code,
			serve,
			branch,
			active_duty,
			pre_1980,
			discharge_char,
			injuries,
			rec_treatment,
			injuries_persist,
			mental_h_need,
			mental_h_issues,
			sexual_assault,
			combat_zone,
			filed_prev,
			eligible,
			email,
			password):

		self.first_name = first_name
		self.last_name = last_name
		self.address_1 = address_1
		self.address_2 = address_2
		self.city = city
		self.state = state
		self.zip_code = zip_code
		self.serve = serve
		self.branch = branch
		self.active_duty = active_duty
		self.pre_1980 = pre_1980
		self.discharge_char = discharge_char
		self.injuries = injuries
		self.rec_treatment = rec_treatment
		self.injuries_persist = injuries_persist
		self.mental_h_need = mental_h_need
		self.mental_h_issues = mental_h_issues
		self.sexual_assault = sexual_assault
		self.combat_zone = combat_zone
		self.filed_prev = filed_prev
		self.eligible = eligible
		self.email = email
		self.password = password

	def insert_veteran(veteran):
		db.session.add(veteran)
		db.session.commit()

	@classmethod
	def get_all_veterans(cls):
		all_veterans = veterans.query.all()
		return all_veterans

	def login(email, password):
		print(email)
		veteran = db.session.query(and_(veterans.email == email, veterans.password == password)).first()
		if veteran:
			return True
		return False

	def get_veteran(email):
		print(email)
		veteran = veterans.query.filter(veterans.email == email).first()
		print(veteran)
		if veteran:
			return veteran
		return False





	@property
	def serialize(self):
		return {
			'id' : self.id,
			'first_name' : self.first_name,
			'last_name' : self.last_name,
			'address_1' : self.address_1,
			'address_2' : self.address_2,
			'city' : self.city,
			'state' : self.state,
			'zip_code' : self.zip_code,
			'serve' : self.serve,
			'branch' : self.branch,
			'active_duty' : self.active_duty,
			'pre_1980' : self.pre_1980,
			'discharge_char' : self.discharge_char,
			'injuries' : self.injuries,
			'rec_treatment' : self.rec_treatment,
			'injuries_persist' : self.injuries_persist,
			'mental_h_need' : self.mental_h_need,
			'mental_h_issues' : self.mental_h_issues,
			'sexual_assault' : self.sexual_assault,
			'combat_zone' : self.combat_zone,
			'filed_prev' : self.filed_prev,
			'eligible' : self.eligible,
			'email' : self.email
		}

class blog_posts(db.Model):
	id = db.Column('post_id', db.Integer, primary_key = True)
	date_posted = db.Column('date_posted', db.DateTime)
	content = db.Column('content', db.Text)

	def __init__(self, date_posted, content):
		self.date_posted = date_posted
		self.content = content

	def insert_post(blog_post):
		db.session.add(blog_post)
		db.session.commit()

	@classmethod
	def get_all_posts(cls):
		posts = blog_posts.query.all()
		return posts

	@property
	def serialize(self):
		return {
			'date_posted' : self.date_posted,
			'content' : self.content
		}




class discussion_posts(db.Model):
	id = db.Column('post_id', db.Integer, primary_key = True)
	date_posted = db.Column('date_posted', db.DateTime)
	content = db.Column('content', db.Text)
	reply_to = db.Column('reply_to', db.Integer)
	category = db.Column('category', db.String(100))

	def __init__(self, date_posted, content, reply_to,category):
		self.date_posted = date_posted
		self.content = content
		self.reply_to = reply_to
		self.category = category

	def insert_discussion_post(discussion_post):
		db.session.add(discussion_post)
		db.session.commit()

	@classmethod
	def get_all_posts(cls):
		posts = discussion_posts.query.all()
		return posts

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'date_posted' : self.date_posted,
			'content' : self.content,
			'reply_to' : self.reply_to,
			'category' : self.category
		}


