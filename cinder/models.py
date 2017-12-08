from mongoengine import *

GENDERS = ('M', 'F')
class Profile(EmbeddedDocument):
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    gender = StringField(max_length=1, choices=GENDERS)
    age = IntField()
    photo = FileField() #GridGS
    bio = StringField()

class User(Document):
    email = EmailField(required=True)
    new_matches = BooleanField()
    password = StringField()
    profile = EmbeddedDocumentField(Profile)
    interested_in = StringField(max_length=1, choices=GENDERS)
    answers = ListField(StringField())
    location = StringField()
    connectionid = StringField()

#now look at mongoengine docs and the first page of the flask book adn figure out how to combine them, i.e how to add functions when getting and setting
