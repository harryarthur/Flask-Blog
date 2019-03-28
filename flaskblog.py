from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
      'author':"Corey Schafer",
      'title' : "Blog Post 1",
      'content': "First post content",
      'date_posted':"April 20 2018"
    },
    {
      'author':"Jane Doe",
      'title' : "Blog Post 2",
      'content': "Second post content",
      'date_posted':"April 21 2018"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')
    

#this conditional is only true if we run this script directly using python
#if running through flask, remember to set environment variables:
# export FLASK_APP=flaskblog.py and
# export FLASK_DEBUG=1 to run in debug mode
if __name__ == '__main__':
    app.run(debug=True)
