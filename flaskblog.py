from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
#When using the sign up and log in forms we need a secret key to protect against modifying cookies
#and forgery attacks etc. app.config is used to set a config value on our application
#You want your secret key to be a good set of random characters.(you can use pythons secret module 
# to generate one).You'll likely want to make this an environment vairable at some point.
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#SQLAlchemy is an ORM (Object relational Mapper) - it allows u to acces our database in 
#an easy to use object oriented way. SQl Alchemyis cool because you can use idfferent databases 
#without changing your python code underneath. So for example, if you want to use an SQLite db for
#testing and a postgres db for production, then all you need to do is pass a different db url for
#sqlalchemy to connect and all the code to CRUD the db will remain the same. sqlite is a file
#on the file system.

#create a DB instance
db = SQLAlchemy(app)
#sqlalchemy lets us represent our database as classes called models like this:

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpeg')
    password = db.Column(db.String(60), nullable=False)
#backref attribute is similiar to adding anothing column to this middle, but what it
#allows us to do is when we have a post we can simply use this author attribute to get the
#user who created the post. The lazy argument just defines how SQLalchemy lods the data
#from the database setting it to True means it will load it as necessary in one go
#capital P in Post because we're referencing the Post class itself
    posts = db.relationship('Post',backref='author',lazy=True)
#double underscore method(dunder methods or magic methods), this specifically is how
#our object is printed whenever we print it out. This function is part of the User class
    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.image_file}')" 


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
#user.id, user is lowercase U because it is refering the table name and the column name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    
    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')" 

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

#this register route has to be able to accept get/post requests
@app.route("/register", methods=['GET', 'POST'])
def register():
#we need to create an instance of the form to send to our application 
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
#and then we can pass this form to a template
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#this conditional is only true if we run this script directly using python
#if running through flask, remember to set environment variables:
# export FLASK_APP=flaskblog.py and
# export FLASK_DEBUG=1 to run in debug mode
if __name__ == '__main__':
    app.run(debug=True)

