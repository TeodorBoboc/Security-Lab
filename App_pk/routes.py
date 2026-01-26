from flask import render_template, url_for, flash, redirect, session
from App_pk import app, db, bcrypt  # Importăm obiectele app și db din __init__.py
from App_pk.forms import RegistrationForm, LoginForm # Importăm clasele din forms.py
from App_pk.models import User, Post # Importăm clasele din models.py

posts=[
    {
        'author':'Boboc Teodor',
        'title':'Blog post 1',
        'content':'Pisici cute',
        'post_date':'Ianuarie 19,2026'
    },

    {
        'author':'Rares Negru',
        'title':'Blog post 2',
        'content':'Caini cute',
        'post_date':'Martie 14,2026'
    },

    {
        'author':'David Hont',
        'title':'Blog post 3',
        'content':'Arici mov',
        'post_date':'Aprilie 6,1123'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title="About")
 
@app.route("/register", methods=['GET', 'POST'])
def register():
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
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Te-ai logat!', 'success')
            session['username'] = 'Teodor'
            return redirect(url_for('home'))
        else:
            flash('Ceva nu a functionat. Verifica e-mailul sau parola!','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("Te-ai delogat.", "info")
    return redirect(url_for('home'))