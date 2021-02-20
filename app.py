

#from jwt_bottle import JWTPlugin, auth_required

from bottle import request,response #,redirect
from bottle import route, run,get,post
from playhouse.shortcuts import model_to_dict


from models import Todo,Users #,Auth
from serializers import TodoSchema
from dotenv import load_dotenv

import os
import json
import  bottle
import jwt
import time


'''
Cargando las variables locales
'''
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
app = bottle.Bottle()


@app.post('/api/auth')
def login_required():

    if request.method == 'POST':

        body_unicode = request.json
        print(body_unicode,type(body_unicode))
        received_json_data = body_unicode

        print(received_json_data)
        #received_json_data = json.loads(body_unicode)

        email = received_json_data.get('email')
        password = received_json_data.get('password')

        #Datos del usuario, actual_json_data
        user = Users.get(email=email)

        if not user.verify(password):
            return "Password incorrect"

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

        final_payload_x = { "user" : 
        { 
            "userName" : user.name, 
            "email" : user.email, 
            "issual_time" : int (ts), 
            "expire_time" : int (ts + 3500) 
        }, 

            "jwtToken" : actual_access_token, 
            "refreshToken" : actual_refresh_token 
        } 


        return final_payload_x

def checkiftokenisvalid(func):

    def wrapper(*args):

  
        #print(request.params.get('HTTP_JWTTOKEN'))

        refreshToken = request.get_header('refreshToken')
        jwtToken = request.get_header('jwtToken')

        payload = jwt.decode(jwtToken, SECRET_KEY, algorithms=["HS256"])

        received_user = payload.get("username") 
        received_expire_time = payload.get("expire_time")            
        received_issual_time = payload.get("issual_time")

        if int(time.time()) > received_expire_time:
            
            print("current tym",int(time.time()))
            print("expire tym",received_expire_time)
            print("issue tym", received_issual_time)
            return 'Token Expired'

                
        
        return func(received_user)

    return wrapper


@app.post('/api/create')
@checkiftokenisvalid
def create(userinfo):

    data = request.json

    user = Users.get(name=userinfo)

    """
    to_do = Todo.create(
        id_user = user,
        title = data['title'],
        description = data['description'],
    )
    """

    Todo.create(
        title= data['title'],
        description= data['description'],
        user_id= user.id
    )

    #to_do.save()
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
        return f"Welcome {userinfo.user}"
    
    else:
        return "Error, not authorized"

if __name__ == '__main__':

    try:
        user = Users.get(name='Hugo', email='hugomontaez@gmail.com')

    except Users.DoesNotExist:
        user = Users.create(name='Hugo', email='hugomontaez@gmail.com', password='123456')
        user.gen_hash()
        user.save()

    app.run(debug=True, reloader=True, port=8000)
