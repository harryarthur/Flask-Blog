from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
#When using the sign up and log in forms we need a secret key to protect against modifying cookies
#and forgery attacks etc. app.config is used to set a config value on our application
#You want your secret key to be a good set of random characters.(you can use pythons secret module 
# to generate one).You'll likely want to make this an environment vairable at some point.
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

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

