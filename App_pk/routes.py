import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, session, request
from App_pk import app, db, bcrypt  # Importăm obiectele app și db din __init__.py
from App_pk.forms import RegistrationForm, LoginForm, UpdateAccountForm,PostForm # Importăm clasele din forms.py
from App_pk.models import User, Post # Importăm clasele din models.py
from flask_login import login_user,logout_user,current_user,login_required

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title="About")
 
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if(form.validate_on_submit()):
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        db.session.add(user)
        db.session.commit()
        flash('Contul dumneavoastra a fost creat! Acum va puteti loga!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Ceva nu a functionat. Verifica e-mailul sau parola!','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Te-ai delogat cu succes",'info')
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.image_file != 'default.jpeg':
                old_picture_path = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        pic_file = None
        if form.picture.data:
            pic_file = save_picture(form.picture.data)
        post = Post(title=form.title.data, 
                    content=form.content.data, 
                    image_post=pic_file,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Postarea ta a fost creată!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)