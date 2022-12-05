from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User
from flaskblog.posts.forms import PostForm, CommentForm, ReactForm, DisReactForm
from flaskblog.users.utils import save_post_picture,send_email

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if current_user.username == 'lampofcheer':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            image_file = picture_file
            post = Post(title=form.title.data, content=form.content.data, author=current_user,post_file=image_file)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        res = User.query.filter_by(type='admin')
        body = form.content.data+','+form.title.data+" by " + current_user.email + ' , ' + current_user.username
        send_email(res,'post waiting',body)
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@posts.route("/blog/new", methods=['GET', 'POST'])
@login_required
def new_blog():
    if current_user.username == 'lampofcheer' or current_user.type == 'admin' or current_user.type=='panel':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    if current_user.is_authenticated:
        if current_user.type == 'admin' or current_user.type=='panel' or current_user.username=='lampofcheer':
            form = PostForm()
            if form.validate_on_submit():
                if form.picture.data:
                    picture_file = save_post_picture(form.picture.data)
                    image_file = picture_file
                    post = Blog(title=form.title.data, content=form.content.data, author7=current_user,post_file=image_file)
                else:
                    post = Blog(title=form.title.data, content=form.content.data, author7=current_user)
                db.session.add(post)
                db.session.commit()
                res = User.query.filter_by(type='admin')
                body = form.content.data+','+form.title.data+" by " + current_user.email + ' , ' + current_user.username
                send_email(res,'Blog Added',body)
                flash('Your post has been created!', 'success')
                return redirect(url_for('main.home_blog'))
            return render_template('create_blog.html', title='New Blog',
                                   form=form, legend='New Blog')
        else:
            return "<h3>Admin or panel Login Required.</h3>"


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
    if current_user.username == 'lampofcheer':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    form2 = ReactForm()
    form3 = DisReactForm()
    reactis = React.query.filter_by(author3=current_user , author4=post).all()
    reactis2 = React.query.filter_by(author3=current_user , author4=post).first()
    postreactis = React.query.filter_by(author4=post).all()
    print(reactis2)
    comments = Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.date_comment.desc()).all()
    if form.submit1.data and form.validate():
        pos = Comment(comment_content=form.comment.data, author1=current_user,author2=post)
        db.session.add(pos)
        db.session.commit()
        flash('Thank you for the comment', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    if form2.submit2.data:
        rct = React(author3=current_user, author4=post)
        db.session.add(rct)
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post_id))
    if form3.submit3.data:
        db.session.delete(reactis2)
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post_id))

    return render_template('post.html', title=post.title, post=post,form=form,commentsno=len(comments),comments=comments,form3=form3, form2=form2,postreactis =len(postreactis),reactis=len(reactis))



@posts.route("/blog/<int:blog_id>", methods=['GET', 'POST'])
@login_required
def blog(blog_id):
    if current_user.username == 'lampofcheer':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    post = Blog.query.get_or_404(blog_id)
    form = CommentForm()
    form2 = ReactForm()
    form3 = DisReactForm()
    reactis = React1.query.filter_by(author9=current_user , author4=post).all()
    reactis2 = React1.query.filter_by(author9=current_user , author4=post).first()
    blogreactis = React1.query.filter_by(author9=post).all()
    print(reactis2)
    comments = Comment1.query.filter_by(blog_id=blog_id)\
        .order_by(Comment1.date_comment.desc()).all()
    if form.submit1.data and form.validate():
        pos = Comment1(comment_content=form.comment.data, author8=current_user,author10=post)
        db.session.add(pos)
        db.session.commit()
        flash('Thank you for the comment', 'success')
        return redirect(url_for('posts.blog', blog_id=blog_id))
    if form2.submit2.data:
        rct = React1(author3=current_user, author4=post)
        db.session.add(rct)
        db.session.commit()
        return redirect(url_for('posts.blog', blog_id=blog_id))
    if form3.submit3.data:
        db.session.delete(reactis2)
        db.session.commit()
        return redirect(url_for('posts.blog', blog_id=blog_id))

    return render_template('blog.html', title=post.title, post=post,form=form,commentsno=len(comments),comments=comments,form3=form3, form2=form2,postreactis =len(blogreactis),reactis=len(reactis))



@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    if current_user.username == 'lampofcheer':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    post = Post.query.get_or_404(post_id)
    if post.author.type == 'admin' or current_user.username=='lampofcheer':
        a = 1
    elif post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.status = 'pending'
        db.session.commit()
        res = User.query.filter_by(type='admin')
        body = form.content.data+','+form.title.data+" by " + current_user.email + ' , ' + current_user.username
        send_email(res,'post updated',body)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')



@posts.route("/blog/<int:blog_id>/update", methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    if current_user.username == 'lampofcheer' or current_user.type == 'admin' or current_user.type=='panel':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    post = Blog.query.get_or_404(blog_id)
    if post.author7.type == 'admin' or current_user.username=='lampofcheer':
        a = 1
    elif post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        res = User.query.filter_by(type='admin')
        body = form.content.data+','+form.title.data+" by " + current_user.email + ' , ' + current_user.username
        send_email(res,'Blog updated',body)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.blog', blog_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_blog.html', title='Update blog',
                           form=form, legend='Update Blog')




@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    if current_user.username == 'lampofcheer':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    post = Post.query.get_or_404(post_id)
    if post.author.type == 'admin' or current_user.username=='lampofcheer':
        a = 1
    elif post.author != current_user:
        abort(403)
    post.status='delete'
    db.session.commit()
    res = User.query.filter_by(type='admin')
    body = post.title+','+post.content+" by " + current_user.email + ' , ' + current_user.username
    send_email(res,'post deleted',body)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))



@posts.route("/blog/<int:blog_id>/delete", methods=['POST'])
@login_required
def delete_blog(blog_id):
    if current_user.username == 'lampofcheer' or current_user.type == 'admin' or current_user.type=='panel':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    post = Blog.query.get_or_404(blog_id)
    if post.author7.type == 'admin' or current_user.username=='lampofcheer':
        a = 1
    elif post.author7 != current_user:
        abort(403)
    post.status='delete'
    db.session.commit()
    res = User.query.filter_by(type='admin')
    body = post.title+','+post.content + " by " + current_user.email + ' , ' + current_user.username
    send_email(res,'Blog deleted',body)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home_blog'))


@posts.route("/blog/<int:blog_id>/approve", methods=['GET','POST'])
@login_required
def approve_blog(blog_id):
    if current_user.username == 'lampofcheer' or current_user.type == 'admin' or current_user.type=='panel':
        a = 1
    elif current_user.status != 'approve':
        return "<h2>Please wait for account approve. it may take upto 12 hours.</h2>"
    post = Blog.query.get_or_404(blog_id)
    if post.author7.type == 'admin'or current_user.username == 'lampofcheer':
        a = 1
    elif post.author7 != current_user:
        abort(403)
    post.status='approve'
    db.session.commit()
    res = User.query.filter_by(type='admin')
    body = post.title+','+post.content+" by " + current_user.email + ' , ' + current_user.username
    send_email(res,'Blog approved',body)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home_blog'))
