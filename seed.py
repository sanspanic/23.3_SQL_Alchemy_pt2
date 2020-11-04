"""seed file to make sample data"""

from models import User, db
from app import app

#create all tables
db.drop_all()
db.create_all()

#if table isn't empty, empty it
User.query.delete() 

#add users
peter = User(first_name='Peter', last_name='Miller', img_url='https://images.unsplash.com/photo-1567201080580-bfcc97dae346?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1100&q=80')
rita = User(first_name='Rita', last_name='Balen', img_url='https://images.unsplash.com/photo-1541689221361-ad95003448dc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1650&q=80')
fergus = User(first_name='Fergus', last_name='Cullen', img_url='https://images.unsplash.com/photo-1587213128862-80345e23a71a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80')

#add new objects to session, so they persist
db.session.add(peter)
db.session.add(rita)
db.session.add(fergus)

#commit otherwise this won't save
db.session.commit()

