from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'qwoidqwidubqwduqw'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page(): 
    """homepage redirects to list of users"""
    return redirect('/users')

@app.route('/users')
def list_all_users(): 
    """list all users"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/add')
def add_new_user(): 
    """renders template to add new user"""
    return render_template('new.html')

@app.route('/users/add', methods=['POST'])
def add_new_user_to_db(): 
    """adds new user to db"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    new_user = User(first_name=first_name,last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id): 
    """display details about individual user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id): 
    """displays form where user can edit info"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_db_with_user_edits(user_id): 
    """updates db with user's edits"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id): 
    """deletes user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


