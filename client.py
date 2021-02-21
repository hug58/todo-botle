
from bottle import request,template,static_file
import bottle

app = bottle.Bottle()

@app.get('/',method=['GET'])
def index():
    return template('./staticfiles/index.html')

@app.get('/register',method=['GET'])
def register():
    return template('./staticfiles/register.html')

@app.get('/notes',method=['GET'])
def notes():
    return template('./staticfiles/notes.html')

@app.get('/static/<dir:path>/<filename:path>')
def server_static(dir,filename):
    print(dir,filename)
    return static_file(filename, root=f'staticfiles/static/{dir}')


if __name__ == '__main__':
    app.run(debug=True, reloader=True, port=5000)
