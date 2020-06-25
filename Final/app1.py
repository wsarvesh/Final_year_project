from flask import Flask, render_template, url_for, redirect, request, flash
import sqlite3 as sql
from flask_bootstrap import Bootstrap
from flask import request, redirect, session, jsonify, flash
from stream_xg import stream
import threading
from twilio.rest import Client


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
		print(keyword)
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
	cur.execute("SELECT * FROM all_tweet WHERE hashtag = ? AND class = ? ",[session['h'],'Relevant'])
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
	cur.execute("SELECT * FROM all_tweet WHERE hashtag = ? AND priority = ? ",[session['h'],'1'])

	rows=cur.fetchall();
	rows.reverse()

	if request.method == 'POST':
		form = request.form
		keyword = form['command']
		if(keyword == 'update'):
			return redirect('/prior')
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

	# the following line needs your Twilio Account SID and Auth Token
	client = Client("AC3964d536be16e00094f027bdd3b3ae30", "98a87736c8ebc28ba22e80628afa16f0")

	try:
		con=sql.connect("tweets.db")
		con.row_factory=sql.Row

	except Error:
		print(Error)

	cur=con.cursor()
	print("key",keyword)
	cur.execute("SELECT * FROM all_tweet where user_id = ?",[keyword])

	rows=cur.fetchall();

	if request.method == 'POST':
		form = request.form
		notifyp = form['command'].split(".")
		print("done on goal", notifyp)
		if(notifyp[0] == 'hosp'):
			print(notifyp[1])
			cur.execute("SELECT * FROM all_tweet where user_id = ?",[notifyp[1]])
			rows=cur.fetchall();
			for row in rows:
				msg = "User Name:" + str(row["user_name"]) + " User Location :"  + str(row["user_location"])+  " Time: "+ str(row["created_at"]) + " Co-oridnates " + str(row["coordinates"]) + " Place : " + str(row["place_name"]) + " Source " + str(row["source"])
				print("msg:"+msg+"\n")
				client.messages.create(to="+918104890460",
                       from_="+15592451737",
                       #body="User Name: {} User Location :{} Time: {} Co-oridnates {} Place : {} Source {}"+row["user_name"]+row["user_location"],row["created_at"],row["coordinates"],row["place_name"],row["source"]))
						body=msg
						)
				account_sid = 'ACb0451e02563a5f905667d93400fa44ef'
				auth_token = 'e2f6d0f7013bad8334c51cce7840b2af'
				client = Client(account_sid, auth_token)

				message = client.messages.create(
				                              from_='whatsapp:+14155238886',
				                              body=msg,
				                              to='whatsapp:+917588926601'
				                          )

				print(message.sid)
		#print("DONE")
		if(notifyp[0] == 'police'):
			client.messages.create(to="+918104890460",
                       from_="+15592451737",
                       body="Report zhala complete!")
		if(notifyp[0] == 'gov'):
			client.messages.create(to="+918104890460",
                       from_="+15592451737",
                       body="Report zhala complete!")
		if(notifyp[0] == 'fire'):
			client.messages.create(to="+918104890460",
                       from_="+15592451737",
                       body="Report zhala complete!")
		if(notifyp[0] == 'ngo'):
			client.messages.create(to="+918104890460",
                       from_="+15592451737",
                       body="Report zhala complete!")
		if(notifyp[0] == 'emerg'):
			client.messages.create(to="+918104890460",
                       from_="+15592451737",
                       body="Report zhala complete!")

	for i in rows:
		print("yo",i["user_id"])

	return render_template('displayinfo.html',keyword=keyword,rows=rows)


if __name__=='__main__':
	app.run(debug=True, threaded=True)
