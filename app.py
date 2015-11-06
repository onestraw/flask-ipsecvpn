from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from forms import AddIpsecSaForm
import xfrm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/add-sa', methods=['GET', 'POST'])
def addsa():
	form = AddIpsecSaForm()
	if request.method=='POST' and form.validate_on_submit():
		input_data = dict((key, request.form.getlist(key)[0]) for key in request.form.keys())
		response = xfrm.add_sa(input_data)
		msg = 'You have submiited the request!\n %s\n' %(response)
		flash(msg)
		return redirect('/add-sa')
	return render_template('add-sa.html', form=form)

sad = []
spd = []

@app.route('/dump-sad', methods=['GET', 'POST'])
def dumpsad():
	global sad
	if request.method == 'GET':
		return render_template('dump-sad.html', result = sad)
	#if request.method=='POST':
	print request.form
	if'delete' in request.form:
		for sa in sad:
			if sa['uuid'] in request.form:
				xfrm.del_sa(sa)
		sad = [sa for sa in sad if sa['uuid'] not in request.form]
	elif 'refresh' in request.form:
		sad = xfrm.parse_sad()
	return redirect('/dump-sad')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    manager.run()
