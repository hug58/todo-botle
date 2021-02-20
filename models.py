

from peewee import (SqliteDatabase, Model, CharField,ForeignKeyField, DateField, DoesNotExist, PrimaryKeyField)
from passlib.hash import pbkdf2_sha512 as hsh 

from hashlib import md5
from dotenv import load_dotenv

import os
import sqlite3


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
rute_db ='ToDo.db'
db = SqliteDatabase(rute_db)




class Users(Model):

    id = PrimaryKeyField(null=False)
    name = CharField(max_length=50,unique=True)
    email = CharField(max_length=200)
    password = CharField(max_length=300)

    def gen_hash(self):
        _secret = md5(SECRET_KEY.encode()).hexdigest()
        _password = md5(self.password.encode()).hexdigest()
        self.password = hsh.hash(_secret + _password)

    def verify(self,password):
        _secret = md5(SECRET_KEY.encode()).hexdigest()
        _password = md5(password.encode()).hexdigest()
        return hsh.verify(_secret+_password, self.password)

    class Meta:
        database = db



class Todo(Model):
    
    id = PrimaryKeyField(null=False)
    user_id = ForeignKeyField(Users,backref="todos")
    title = CharField()
    description = CharField()

    class Meta:
        database = db
        db_table = "todos"


    @staticmethod
    def create(**args):
        query = "INSERT INTO todos ('user_id','title','description')VALUES ({user_id},'{title}','{description}')".format(**args)
        conn = sqlite3.connect(rute_db)

        c = conn.cursor()
        c.execute(query)

        conn.commit()
        conn.close()


db.create_tables([Todo,Users])
