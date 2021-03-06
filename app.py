from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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

#USER ROUTES 

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
    all_posts = User.query.all
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

#POSTS ROUTES

@app.route('/users/<int:user_id>/posts/new')
def show_form_to_add_new_post(user_id): 
    """shows form by which user can add new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('posts/new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id): 
    """adds new post to db and redirects to user detail page"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=request.form['title'], 
                    content=request.form['content'], 
                    user=user, 
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id): 
    """shows individual post based on ID of post"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    
    return render_template('posts/post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id): 
    """shows individual post form to be edited"""
    post = Post.query.get_or_404(post_id)

    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def add_edited_post_to_db(post_id): 
    """sends edited post to db and redirects to post view page"""
    post = Post.query.get_or_404(post_id)

    post.title=request.form['title']
    post.content=request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f'Post "{post.title}" was successfully edited')

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id): 
    """deletes post"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f'Post "{post.title}" was successfully deleted')

    return redirect(f'/users/{post.user_id}')

#TAGS routes

@app.route('/tags')
def show_tags(): 
    """lists all tags, with links to the tag detail page"""
    tags = Tag.query.all()

    return render_template('tags/show_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id): 
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tags/tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def add_tag(): 
    """show a form to add a new tag"""
    
    return render_template('tags/add_tag.html')

@app.route('/tags/new', methods=['POST'])
def add_tag_to_db(): 
    """Process add form, add tag, and redirect to tag list."""
    new_tag = Tag(name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()

    flash(f"Tag '{new_tag.name}' was successfully added")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id): 
    """Show edit form for a tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit_tag.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id): 
    """Process edit form, edit tag, and redirects to the tags list."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' was successfully edited")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")
    




