from flask import Flask, render_template, url_for, redirect, request
import sqlite3 as sql
from flask_bootstrap import Bootstrap
from flask import request, redirect, session, jsonify, flash
from stream_xg import stream


class Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        stream()

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET','POST'])
def homepage():
	if request.method == 'POST':
		form = request.form
		global k
		k = form['query']
		if((k.strip())):
			return redirect('/rev')
	return render_template('homepage.html')

@app.route('/rev',  methods=['GET', 'POST'])
def rev():
	try:
		con=sql.connect("tweets.db")
		con.row_factory=sql.Row

	except Error:
		print(Error)

	print(k)

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

	t = Thread()
    t.start()

	cur=con.cursor()
	cur.execute("SELECT text,user_location FROM all_tweet")

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
	cur.execute("SELECT text,user_location FROM tweets")

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
	cur.execute("SELECT * FROM tweets where text = ?",[keyword])

	rows=cur.fetchall();
	print(rows)
	print(type(rows))
	return render_template('displayinfo.html',keyword=keyword,rows=rows)


if __name__=='__main__':
    app.run(debug=True)
