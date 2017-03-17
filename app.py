#!flask/bin/python

from flask import Flask
from flask import request
from flask import jsonify
import json
from database import *
import datetime
from datetime import datetime
from fill_pdf import *
import fill_pdf
import requests
from operator import itemgetter


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
	return jsonify({'success' : true})

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
	return jsonify({'success' : true})

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
	if eligible == None:
		eligible = ""
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

	veterans.insert_veteran(veteran)

	return jsonify("{success : true}")

#veteran PDF
@app.route('/api/veteran/pdf', methods=['GET'])
def get_pdf():
	email = request.args.get('email')
	veteran = veterans.get_veteran(email)
	fill_pdf.execute(veteran)
	url = "http://50.116.44.47:8080/" + email + "_VBA-21-526EZ-ARE.pdf"
	return jsonify({'url' : url}) 


#login
@app.route('/api/login', methods=['POST'])
def login():
	user = request.args.get('email')
	password = request.args.get('password')

	result = veterans.login(user, password)

	return jsonify({'result' : result})

#forum search
@app.route('/api/veteran/customizer')
def forum_search():
	veteran = veterans.get_veteran(request.args.get('email'))
	search_terms = []
	objects = []
	
	if veteran.branch:
		search_terms.append(veteran.branch)

	if veteran.discharge_char:
		search_terms.append(veteran.discharge_char)

	if veteran.injuries:
		search_terms.append(veteran.injuries)

	if veteran.mental_h_issues:
		search_terms.append(veteran.mental_h_issues)

	if veteran.combat_zone:
		search_terms.append("war")

	for term in search_terms:
		url = "http://forum.theserviceconnection.org/search/query.json?term=" + term
		r = requests.get(url)
		check = json.loads(r.text)
		if check['posts']:
			objects.append(r.text)

	return jsonify(objects)

#top 3 accounts like you
@app.route('/api/veteran/yourtop3')
def top_three():
	email = request.args.get("email")
	user = veterans.get_veteran(email)
	print(user)

	o_veterans = veterans.get_all_veterans()
	veteran_list = []

	for veteran in o_veterans:
		points = 0

		if veteran.branch and user.branch:
			if veteran.branch in user.branch:
				points += 1
		
		if veteran.discharge_char and user.discharge_char:
			if veteran.discharge_char in user.discharge_char:
				points += 1
		
		if veteran.injuries and user.injuries:
			if veteran.injuries in user.injuries:
				points += 1

		if veteran.mental_h_issues and user.mental_h_issues:
			if veteran.mental_h_issues in user.mental_h_issues:
				points += 1

		if veteran.combat_zone and user.combat_zone:
			if veteran.combat_zone == user.combat_zone:
				points += 1

		score = (points / 5) * 100
		if veteran.email != user.email:
			veteran_list.append([veteran.email, score])

	veteran_list_sorted = sorted(veteran_list, key=itemgetter(1), reverse=True)

	top3 = veteran_list_sorted[:3]
	api_key = "3480b7601125e759b59927445f9a0f9b5d96008aa7ce19d9d577e1209cc858e8"
	data = []
	for v in top3:
		url = "http://forum.theserviceconnection.org/admin/users/list/active.json?" + "filter=" + v[0] + "&api_key=" + api_key
		r = requests.get(url)
		d = json.loads(r.text)
		d[0]["score"] = v[1]
		data.append(d)

	return jsonify(data)




def get_file_contents(filename):
	with open(filename) as f:
		return f.read()

if __name__ == '__main__':
	db.init_app(app)
	app.run(debug=True)
