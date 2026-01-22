#API-ul
from flask import Flask,render_template,url_for,flash,redirect,session
from forms import RegistrationForm,LoginForm
app=Flask(__name__)

app.config['SECRET_KEY']='1234567'

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
        'content':'Caini negrii',
        'post_date':'Martie 14,2026'
    },

    {
        'author':'David Hont',
        'title':'Blog post 3',
        'content':'India suicide',
        'post_date':'Aprilie 69,1945'
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
        flash(f'Cont creeat pentru {form.username.data}! ','success')
        return redirect(url_for('home'))
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
if __name__=="__main__":
    app.run(debug=True)