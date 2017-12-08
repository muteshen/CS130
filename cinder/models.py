from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash

GENDERS = ('M', 'F')
class Profile(EmbeddedDocument):
    first = StringField(max_length=50)
    last = StringField(max_length=50)
    gender = StringField(max_length=1, choices=GENDERS)
    age = IntField()
    photo = FileField() #GridGS
    bio = StringField()

class User(Document):
    email = EmailField(required=True)
    new_matches = BooleanField()
    password_hash = StringField()
    profile = EmbeddedDocumentField(Profile)
    interested_in = StringField(max_length=1, choices=GENDERS)
    answers = ListField(StringField())
    location = StringField()
    connectionid = StringField()
    cid = IntField()
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

    # # Flask-Login integration
    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False
    #
    # def get_id(self):
    #     return str(self.id)
    #
    # @staticmethod
    # def validate_login(password_hash, password):
    #     return check_password_hash(password_hash, password)
