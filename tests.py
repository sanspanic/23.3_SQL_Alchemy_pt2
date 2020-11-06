from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user & post."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Testus", last_name="Testman", img_url='www.google.com')
        post = Post(title="Test Post", content="pigs are great", user=user)

        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_all_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testman', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testman', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Testina", "last_name": "Testwoman", "img_url": 'www.differenturl.com'}
            resp = client.post("/users/add", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Testwoman", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "Amended", "last_name": "Testwoman", "img_url": 'www.google.com'}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Amended", html)

class PostsViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample post & user."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Testus", last_name="Testman", img_url='www.google.com')
        post = Post(title="Test Post", content="pigs are great", user=user)

        db.session.add(user)
        db.session.commit()
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_form_to_add_new_post(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testman', html)

    #I don't understand why the below test works even when I remove "user". I thought "user" is needed to create a post (in app.py, I create the post with title, content and user)
    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "New Post", "content": "Will this work?", "user": self.user}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Post", html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('pigs are great', html)

    def test_show_edit_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("by user Testus Testman", html)

    def test_add_edited_post_to_db(self):
        with app.test_client() as client:
            d = {"title": "Edited Post", "content": "Will this edit work?", "user": self.user}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("was successfully edited", html)

    #equally, here, I don't understand why the test still seems like it is deleting something and works, even when I delete 'd'. I thought the database wouldn't know what to delete without the id of the post.
    def test_add_edited_post_to_db(self):
        with app.test_client() as client:
            d = {"id":self.post_id}
            resp = client.post(f"/posts/{self.post_id}/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("was successfully deleted", html)





    




    



