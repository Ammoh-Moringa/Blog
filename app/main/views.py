from flask import (render_template, request, redirect, 
                   url_for, abort)
from . import main
from ..models import User, Comment, Post, Subscribers
from flask_login import login_required, current_user
from .forms import (UpdateProfile, PostForm, 
                    CommentForm, UpdatePostForm)
from datetime import datetime
# import bleach
from .. import db
from ..requests import get_quote
from ..email import welcome_message, notification_message

@main.route("/", methods = ["GET", "POST"])
def index():
    posts = Post.get_all_posts()
    quote = get_quote()

    if request.method == "POST":
        new_sub = Subscribers(email = request.form.get("subscriber"))
        db.session.add(new_sub)
        db.session.commit()
        welcome_message("Blog welcomes you to this platform", 
                        "email/welcome", new_sub.email)
    return render_template("index.html",
                            posts = posts,
                            quote = quote)

@main.route("/post/<int:id>", methods = ["POST", "GET"])
def post(id):
    post = Post.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(post_id = id).all()
    comment_form = CommentForm()
    comment_count = len(comments)

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        comment_form.comment.data = ""
        comment_alias = comment_form.alias.data
        comment_form.alias.data = ""
        if current_user.is_authenticated:
            comment_alias = current_user.username
        new_comment = Comment(comment = comment, 
                            comment_at = datetime.now(),
                            comment_by = comment_alias,
                            post_id = id)
        new_comment.save_comment()
        return redirect(url_for("main.post", id = post.id))

    return render_template("post.html",
                            post = post,
                            comments = comments,
                            comment_form = comment_form,
                            comment_count = comment_count)


@main.route("/profile/<int:id>", methods = ["POST", "GET"])
def profile(id):
    user = User.query.filter_by(id = id).first()
    posts = Post.query.filter_by(user_id = id).all()

    if request.method == "POST":
        new_sub = Subscribers(email = request.form.get("subscriber"))
        db.session.add(new_sub)
        db.session.commit()
        welcome_message("Thank you for subscribing to the CM blog", 
                        "email/welcome", new_sub.email)

    return render_template("profile/profile.html",
                            user = user,
                            posts = posts)

@main.route("/profile/<int:id>/<int:post_id>/delete")
@login_required
def delete_post(id, post_id):
    user = User.query.filter_by(id = id).first()
    post = Post.query.filter_by(id = post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("main.profile", id = user.id))

@main.route("/profile/<int:id>/update", methods = ["POST", "GET"])
@login_required
def update_profile(id):
    user = User.query.filter_by(id = id).first()
    form = UpdateProfile()
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.profile", id = id))
    
    return render_template("profile/update.html",
                            user = user,
                            form = form)