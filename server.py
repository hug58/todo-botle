


from bottle import request,response

from models import Todo,Users 
from serializers import TodoSchema
from dotenv import load_dotenv

import os
import json
import bottle
import jwt
import time


'''
Cargando las variables locales
'''
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
app = bottle.Bottle()


@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


def checkiftokenisvalid(func):
    '''
    decorator that checks if the token has expired or not
    '''
    def wrapper(*args):

  
        #refreshToken = request.get_header('refreshToken')
        jwtToken = request.get_header('jwtToken')

        payload = jwt.decode(jwtToken, SECRET_KEY, algorithms=['HS256'])

        received_user = payload.get('username') 
        received_expire_time = payload.get('expire_time')            
        received_issual_time = payload.get('issual_time')

        if int(time.time()) > received_expire_time:
            
            print('current tym',int(time.time()))
            print('expire tym',received_expire_time)
            print('issue tym', received_issual_time)
            return 'Token Expired'

                
        
        return func(received_user)

    return wrapper


@app.post('/api/auth/register')
def register():  
    if request.method == 'POST':
        received_json_data = request.json

        try:
            user = Users.create(
                name= received_json_data.get('username'), 
                email= received_json_data.get('email'), 
                password= received_json_data.get('password'))
            
            user.gen_hash()
            user.save()

            response.status = 201
            return {'status': f'user {user.name} successfully registered!'}

        except:
            return {'status': f'user {received_json_data.get("username")}  already registered'}
            

    else:
        return {'status': f'wrong method, {request.method}'}


@app.post('/api/auth/login')
def login_required():
    if request.method == 'POST':

        if request.json:
            received_json_data = request.json
        elif request.body:
            received_json_data = json.load(request.body)
        else:
            response.status = 400
            return {'status': 'Body no found'}

        email = received_json_data.get('email')
        password = received_json_data.get('password')

        user = Users.get(email=email)

        if not user.verify(password):
            return 'Password incorrect'

        refresh_token_content = {}

        if user:
            refresh_token_content = {
            'user_id': user.id,
            'username': user.name,
            'password': user.password,
            'email': user.email,
        }

        refresh_token = {
            'refreshToken': jwt.encode(refresh_token_content,SECRET_KEY,algorithm='HS256')
        }

        temp = refresh_token.get('refreshToken')
        actual_refresh_token = temp

        ts = int(time.time())
        access_token_content = {
            'username': user.name,
            'password': user.password,
            'email':user.email,
            'issual_time': ts,
            'expire_time': ts + 3500
        }


        jwt_token = { 'token' : jwt.encode (access_token_content, SECRET_KEY,algorithm='HS256')} 
        u = jwt_token.get ( 'token' ) 
        actual_access_token = u
        ts = float (time.time ())

        final_payload_x = { 'user' : 
        { 
            'userName' : user.name, 
            'email' : user.email, 
            'issual_time' : int (ts), 
            'expire_time' : int (ts + 3500) 
        }, 

            'jwtToken' : actual_access_token, 
            'refreshToken' : actual_refresh_token 
        } 

        return final_payload_x


@app.post('/api/create')
@checkiftokenisvalid
def create(userinfo):
    data = request.json
    user = Users.get(name=userinfo)

    '''
    peewee has a bug when I try to use a foreign key, so 
    I had to make my own static method in SQL code
    '''

    '''
    to_do = Todo.create(
        id_user = user,
        title = data['title'],
        description = data['description'],
    )
    to_do.save()
    '''

    Todo.create(
        title= data['title'],
        description= data['description'],
        user_id= user.id
    )
    response.status = 201
    return data


@app.get('/api/all')
@checkiftokenisvalid
def list_to_do(userinfo):
    id_user = Users.get(name=userinfo)
    query = Todo.select().where(id_user)

    schema = TodoSchema()
    result = schema.dump(query,many=True)
    return {'data':result}


@app.post('/api')
@checkiftokenisvalid
def index(userinfo):

    if user:
        return f'Welcome {userinfo.user}'
    
    else:
        return 'Error, not authorized'

if __name__ == '__main__':

    try:
        user = Users.get(name='Hugo', email='hugomontaez@gmail.com')

    except Users.DoesNotExist:


        user = Users.create(
            name='Hugo', 
            email='hugomontaez@gmail.com', 
            password='123456')
        
        user.gen_hash()
        user.save()

    app.run(debug=True, reloader=True, port=8000)
