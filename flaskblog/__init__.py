from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes