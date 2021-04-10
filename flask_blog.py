from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#url_for finds the exact routes for us so that we don't worry about it in main


app = Flask(__name__)
#We need to set a secret key which protects against modifying cookies and cross-site requests and forgery attacks
app.config['SECRET_KEY'] = '7186bfb3da5c04264f9216cf0ba12cf99812977d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'     #Relative path with /// from current file
db = SQLAlchemy(app)        #Creating an database instance


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        '''	To get called by built-int repr() method to return a machine readable representation of a type.
        What this function returns is displayed when we access the data in this table.'''
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.content}', '{self.date}')"

#dummy data as it should be fetched from database
posts = [{
    'author' : 'George RR Martin',
    'title' : 'Winds of Winter Update',
    'content' : 'Don\'t Bother! Read something else please!',
    'date' : '31/03/2021'
},
{
    'author' : 'JK Rowling',
    'title' : 'The Cuckoo\'s Calling',
    'content' : 'Won Something! Again!! Great Day ;)',
    'date' : '29/03/2021'
},
{
    'author' : 'George RR Martin',
    'title' : 'Winds of Winter Update',
    'content' : 'Releasing Soon! I am working as hard as possible!!',
    'date' : '15/03/2021'
}]

@app.route('/')     #Root Page
@app.route('/home')
def home():
    return render_template('home.html', title = 'Home Page',posts = posts)
# The Templating Engine that Flask uses is called is k/a Jinja

@app.route('/about')     #About Page
def about():
    return render_template('about.html', title = 'About')

@app.route('/register', methods = ['GET', 'POST'])     #Registration Page
def register():
    form = RegistrationForm()
    #hidden_tag(): Adds Cross Site Request Forgery Token
    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}.', 'success')
        return redirect(url_for('home'))     #url_for takes the name of method like home, register, login not html page
    return render_template('register.html', title = 'Signup', form = form)

@app.route('/login', methods = ['GET', 'POST'])     #Login Page
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == '12345':
            flash(f'Login Successful.', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Check Username and Password', 'danger')
    return render_template('login.html', title = 'Signin', form = form)

if __name__ == '__main__':
    app.run(debug = True)
# set FLASK_DEBUG=1 in cmd

'''SQL Alchemy lets us represent our database structure as classes which are called models. Each class is a table
in the database. '''