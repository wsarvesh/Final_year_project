from flask import Flask, render_template, url_for, redirect, request, flash
import sqlite3 as sql
from flask_bootstrap import Bootstrap
from flask import request, redirect, session, jsonify, flash
from stream_xg import stream
import threading


class Thread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		stream(h)

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = "abc"


@app.route('/', methods=['GET','POST'])
def homepage():
	t = Thread()
	session['h'] = "-1"
	global h
	h = "-1"
	t.start()
	t.join()
	if request.method == 'POST':
		form = request.form
		h = form['query']
		#print("searched for     :",h)
		session['h'] = h
		if((h.strip()) and h != "-1"):
			t = Thread()
			t.start()
			return redirect('/rev')
		else:
			flash("Oops, Found Nothing!")
	return render_template('homepage.html')

# def pt():
# 	return h

@app.route('/rev',  methods=['GET', 'POST'])
def rev():
	try:
		con=sql.connect("tweets.db")
		con.row_factory=sql.Row

	except Error:
		print(Error)
	# h = session['h']
	print(session['h'])

	if request.method == 'POST':
		form = request.form
		keyword = form['command']
		if(keyword == 'update'):
			return redirect('/rev')
		if(keyword == 'priority'):
			return redirect('/prior')
		if(keyword == 'search'):
			return redirect('/')
		if(keyword == 'back'):
			return redirect('/rev')
		else:
			return about(keyword)

	cur=con.cursor()
	cur.execute("SELECT text,user_location FROM all_tweet WHERE hashtag = ? AND class = ? ",[session['h'],'Relevant'])
	rows=cur.fetchall();
	#print(type(rows))
	rows.reverse()
	i=0
	for row in rows:
		i+=1
	print(i)

	return render_template('rev.html', rows=rows)

@app.route('/prior',  methods=['GET', 'POST'])
def prior():
	try:
		con=sql.connect("tweets.db")
		con.row_factory=sql.Row

	except Error:
		print(Error)

	cur=con.cursor()
	cur.execute("SELECT text,user_location FROM all_tweet WHERE hashtag = ? AND priority = ? ",[session['h'],'1'])

	rows=cur.fetchall();
	rows.reverse()

	if request.method == 'POST':
		form = request.form
		keyword = form['command']
		if(keyword == 'update'):
			return redirect('/priority')
		if(keyword == 'relevant'):
			return redirect('/rev')
		if(keyword == 'search'):
			return redirect('/')
		if(keyword == 'back'):
			return redirect('/rev')
		else:
			#return render_template('about.html', keyword=keyword)
			#return redirect('/about', keyword=keyword)
			return about(keyword)

	return render_template('prior.html', rows=rows)

@app.route('/about', methods=['GET', 'POST'])
def about(keyword):
	try:
		con=sql.connect("tweets.db")
		con.row_factory=sql.Row

	except Error:
		print(Error)

	cur=con.cursor()
	cur.execute("SELECT * FROM all_tweet where text = ?",[keyword])

	rows=cur.fetchall();
	print(rows)
	print(type(rows))
	return render_template('displayinfo.html',keyword=keyword,rows=rows)


if __name__=='__main__':
	app.run(debug=True, threaded=True)