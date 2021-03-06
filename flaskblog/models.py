from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return none
        return User.query.get(user_id)



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
