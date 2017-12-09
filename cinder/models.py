from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

GENDERS = ('M', 'F', 'N')
class Profile(EmbeddedDocument):
    first = StringField(max_length=50)
    last = StringField(max_length=50)
    gender = StringField(max_length=1, choices=GENDERS)
    birthday = DateTimeField()
    photo = FileField() #GridGS
    bio = StringField()

class User(UserMixin, Document):
    cid = ReferenceField('Connection')
    email = EmailField(required=True)
    new_matches = BooleanField()
    password_hash = StringField()
    facebook = StringField()
    profile = EmbeddedDocumentField(Profile, required=True)
    interested_in = StringField(max_length=1, choices=GENDERS, required=True)
    answers = ListField(StringField())
    location = StringField()
    # login = StringField(max_length=80, unique=True)

    @property
    def password(self):
        raise AttributeError("password unreadable")

    #can just set with User.password = password and it will be auto hashed
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @login_manager.user_loader
    def load_user(uid):
        return User.objects(id=uid).first()

class Connection(Document):
    #_id = StringField()
    #uid = ReferenceField(required=True, unique=True)
    liked_you = SortedListField(ReferenceField(User))
    swiped = SortedListField(ReferenceField(User))

class Match(Document):
    #_id = StringField()
    uid1 = ReferenceField(User, required=True)
    uid2 = ReferenceField(User, required=True)
    match_date = DateTimeField(required=True)
    feedback_id = ReferenceField('Feedback')

class Response(EmbeddedDocument):
    date = DateTimeField(required=True)
    from_uid1 = StringField()
    from_uid2 = StringField()

class Feedback(Document):
    #_id = StringField()
    uid1 = ReferenceField(User, required=True)
    uid2 = ReferenceField(User, required=True)
    response = ListField(EmbeddedDocumentField(Response))
