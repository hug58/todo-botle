
from bottle import request,response,template,static_file,redirect

app = bottle.Bottle()

@app.get('/',method=['GET'])
def index():
    return template('./client/index.html')

@app.get('/notes',method=['GET'])
def notes():
    return template('./client/notes.html')

@app.get('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./client/static')


if __name__ == '__main__':
    app.run(debug=True, reloader=True, port=8080)
