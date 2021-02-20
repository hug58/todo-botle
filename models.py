

from peewee import (SqliteDatabase, Model, CharField,ForeignKeyField, DateField, DoesNotExist)
from passlib.hash import pbkdf2_sha512 as hsh 

from hashlib import md5
from dotenv import load_dotenv

import os

load_dotenv()

db = SqliteDatabase('ToDo.db')




class Users(Model):

    name = CharField(max_length=50)
    email = CharField(max_length=200)
    password = CharField(max_length=300)

    def gen_hash(self):
        _secret = md5(os.getenv('SECRET_KEY').encode()).hexdigest()
        _password = md5(self.password.encode()).hexdigest()
        self.password = hsh.hash(_secret + _password)

    def verify(self,password):
        _secret = md5(os.getenv('SECRET_KEY').encode()).hexdigest()
        _password = md5(password.encode()).hexdigest()
        return hsh.verify(_secret+_password, self.password)

    class Meta:
        database = db



class Todo(Model):
    
    user_id = ForeignKeyField(Users,backref="todo")
    title = CharField()
    description = CharField()

    class Meta:
        database = db



db.create_tables([Todo,Users])
