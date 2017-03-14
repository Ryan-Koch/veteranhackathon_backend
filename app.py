#!flask/bin/python

from flask import Flask
from flask import request
from flask import jsonify
import json
from database import *
import datetime
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vetbenefits.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
	return "Goodbye world"

#Blog routes
@app.route('/api/blog', methods=['POST'])
def add_blog_post():
	print("lol adding post")
	post = blog_posts(datetime.now(), request.args.get('content'))
	blog_posts.insert_post(post)
	return jsonify("{success : true}")

@app.route('/api/blog', methods=['GET'])
def get_blog_posts():
	posts = blog_posts.get_all_posts()
	#print(posts)
	return jsonify(posts_list=[post.serialize for post in posts])

#Posts routes
@app.route('/api/discussion', methods=['GET'])
def get_discussion_posts():
	posts = discussion_posts.get_all_posts()
	return jsonify(posts_list=[post.serialize for post in posts])

@app.route('/api/discussion', methods=['POST'])
def add_discussion_post():
	print("lol adding post")
	date_posted = datetime.now()
	content = request.args.get('content')
	reply_to = request.args.get('reply_to')
	
	if reply_to == None:
		reply_to = ""

	print("Reply to " + reply_to)
	category = request.args.get('category')
	post = discussion_posts(date_posted, content, reply_to, category)
	blog_posts.insert_post(post)
	return jsonify("{success : true}")

#Veteran routes

@app.route('/api/veteran', methods=['GET'])
def get_veteran():
	veteran = veterans.get_veteran(request.args.get('email'))
	print(veteran)
	return jsonify(veteran.serialize)

@app.route('/api/veteran', methods=['POST'])
def insert_veteran():
	first_name = request.args.get('first_name')
	last_name = request.args.get('last_name')
	address_1 = request.args.get('address_1')
	address_2 = request.args.get('address_2')
	city = request.args.get('city')
	state = request.args.get('state')
	zip_code = request.args.get('zip_code')
	serve = request.args.get('serve')
	branch = request.args.get('branch')
	active_duty = request.args.get('active_duty')
	pre_1980 = request.args.get('pre_1980')
	discharge_char = request.args.get('discharge_char')
	injuries = request.args.get('injuries')
	rec_treatment = request.args.get('rec_treatment')
	injuries_persist = request.args.get('injuries_persist')
	mental_h_need = request.args.get('mental_h_need')
	mental_h_issues = request.args.get('mental_h_issues')
	sexual_assault = request.args.get('sexual_assault')
	combat_zone = request.args.get('combat_zone')
	filed_prev = request.args.get('filed_prev')
	eligible = request.args.get('eligible')
	email = request.args.get('email')
	password = request.args.get('password')

	veteran = veterans(first_name,
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
		password)

	print(veteran)

	veterans.insert_veteran(veteran)

	return jsonify("{success : true}")

#login
@app.route('/api/login', methods=['POST'])
def login():
	user = request.args.get('email')
	password = request.args.get('password')

	result = veterans.login(user, password)

	return jsonify("{ result : " + str(result) + " }")


if __name__ == '__main__':
	db.init_app(app)
	app.run(debug=True)