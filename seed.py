"""seed file to make sample data"""

from models import User, Post, Tag, PostTag, db
from app import app

def drop_everything():
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()

#create all tables
drop_everything()
#db.drop_all()
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

#add blog posts
f_post_1 = Post(title='1st Post', content='afubewihfb wifbwief weif bwefubweifw', user_id = 3)
f_post_2 = Post(title='2nd Post', content='afuafebewihfb wifbwief weif bwefubweifw', user_id = 3)
f_post_3 = Post(title='3rd Post', content='afaaaaubewihfb wifbwief weif bwefubweifw', user_id = 3)

r_post_1 = Post(title='Lalala', content='afaaaaubewihfb wifbwief feweif bwefubweifw', user_id = 2)
r_post_2 = Post(title='Shalatrala', content='afaaaaubewihfb wifbwigweef weif bwefubweifw', user_id = 2)

#add new objects to session & commit
db.session.add_all([f_post_1, f_post_2, f_post_3, r_post_1, r_post_2])
db.session.commit()

#add tags
t1 = Tag(name='inspiring')
t2 = Tag(name='awesome')
t3 = Tag(name='hopeful')
t4 = Tag(name='OMG')

#add new objects to session & commit
db.session.add_all([t1,t2,t3,t4])
db.session.commit()

#add tags to posts
pt1 = PostTag(post_id=1, tag_id=4)
pt2 = PostTag(post_id=2, tag_id=4)
pt3 = PostTag(post_id=3, tag_id=4)
pt4 = PostTag(post_id=1, tag_id=1)
pt5 = PostTag(post_id=1, tag_id=2)
pt6 = PostTag(post_id=5, tag_id=3)

#add new objects to session & commit
db.session.add_all([pt1,pt2,pt3,pt4,pt5,pt6])
db.session.commit()

