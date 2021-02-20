
from bottle import request,template,static_file
import bottle

app = bottle.Bottle()

@app.get('/',method=['GET'])
def index():
    return template('./client/index.html')

@app.get('/notes',method=['GET'])
def notes():
    return template('./client/notes.html')

@app.get('/static/<dir:path>/<filename:path>')
def server_static(dir,filename):
    print(dir,filename)
    return static_file(filename, root=f'client/static/{dir}')


if __name__ == '__main__':
    app.run(debug=True, reloader=True, port=5000)
