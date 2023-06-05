from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.post import Post
from flask_app.models.user import User
from datetime import datetime


@app.route('/save_news', methods=['POST'])
def save_news():
    print(request.form)
    data = {
        "title": request.form['title'],
        "source": request.form['source'],
        "description": request.form['description'],
        "content": request.form['content'],
        "url": request.form['url'],
        "image": request.form['image'],
        "published_date": request.form['published_date'],
        "user_id": session['id']
    }
    Post.save_news(data)
    return 'ok'


@app.route('/archive/<int:id>')
def show_archive(id):
    archive = User.get_one(id)
    user = User.get_user_archive(id)
    followed = User.get_followers(id)
    follower = User.get_followed(id)
    return render_template('archive.html', user=user, followed=followed, archive=archive, follower=follower)


@app.route('/archive_remove', methods=['POST'])
def archive_remove():
    print(request.form)
    Post.delete_post(request.form)
    return 'ok'
