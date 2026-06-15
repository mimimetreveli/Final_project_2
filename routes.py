from flask import render_template, redirect, flash, request, abort, url_for
from ext import app, db
from forms import RegisterForm, LoginForm, PostForm
from models import User, Post, School
from flask_login import login_user, logout_user, login_required, current_user
from os import path


@app.route("/")
@login_required
def home():
    posts = Post.query.filter_by(school_id=current_user.school_id).order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
@login_required
def post_details(post_id):
    p = Post.query.get_or_404(post_id)
    if p.school_id != current_user.school_id:
        return abort(403)
    return render_template("details.html", p=p)


@app.route("/add_post", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_p = Post(
            title=form.title.data,
            content=form.content.data,
            school_id=current_user.school_id,
            user_id=current_user.id,
            img=None
        )

        file = form.image.data
        if file and file.filename != '':
            # Safeguard static directory context paths
            img_dir = path.join(app.root_path, "static", "images")
            if not path.exists(img_dir):
                import os
                os.makedirs(img_dir)

            file_directory = path.join(img_dir, file.filename)
            file.save(file_directory)
            new_p.img = file.filename

        new_p.create()
        flash("Your post has been successfully shared with your school feed!")
        return redirect(url_for("home"))

    return render_template("add_post.html", form=form, heading="Create New School Post")


@app.route("/like_post/<int:post_id>")
@login_required
def like_post(post_id):
    p = Post.query.get_or_404(post_id)
    if p.school_id != current_user.school_id:
        return abort(403)

    if p in current_user.liked_posts:
        current_user.liked_posts.remove(p)
    else:
        current_user.liked_posts.append(p)

    db.session.commit()
    return redirect(request.referrer or url_for("home"))


@app.route("/delete_post/<int:post_id>")
@login_required
def delete_post(post_id):
    p = Post.query.get_or_404(post_id)
    if p.user_id != current_user.id:
        return abort(403)

    p.delete()
    flash("Post removed successfully.")
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegisterForm()
    if form.validate_on_submit():
        email_string = form.email.data.strip().lower()
        domain_part = email_string.split("@")[0]

        target_school = School.query.filter_by(domain=domain_part).first()
        if not target_school:
            target_school = School(domain=domain_part)
            target_school.create()

        new_user = User(
            name=form.name.data,
            surname=form.surname.data,
            student_id=form.student_id.data,
            grade=form.grade.data,
            email=email_string,
            school_id=target_school.id
        )
        new_user.set_password(form.password.data)
        new_user.create()

        flash("Registration successful! You can now log in.")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("home"))
        flash("Invalid email or password.")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/about")
def about():
    return render_template("about.html")