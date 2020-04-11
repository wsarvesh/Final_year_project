from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask import request, redirect, session, jsonify, flash


app = Flask(__name__)
Bootstrap(app)

@app.route('/index')
def index():
	fruits = ['Apple','Orange','Mango']
	return render_template('index.html', fruits=fruits)
	#return redirect(url_for("about"))
	
@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/', methods=['GET','POST'])
def homepage():
	if request.method == 'POST':
		form = request.form
		keyword = form['query']
		if((keyword.strip())):
			return redirect('/about')
	return render_template('homepage.html')
	
@app.route('/details')
def details():
	return render_template('details.html')
	
@app.route('/table')
def table():
	return render_template('table.html')
	
if __name__ == '__main__':
    app.run(debug=True, port = 5001)