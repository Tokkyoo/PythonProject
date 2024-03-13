import sqlite3
from flask import Flask, render_template, request, make_response, redirect, g

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def valid_login(username, password):
    # Cette fonction devrait vérifier si le nom d'utilisateur et le mot de passe sont valides.
    # Vous pouvez implémenter la validation selon vos besoins.
    return username == 'admin' and password == 'password'


def log_the_user_in(username):
    # Cette fonction pourrait enregistrer l'utilisateur connecté dans une session ou effectuer d'autres actions.
    resp = make_response(redirect('/animelist'))
    resp.set_cookie('username', username)
    return resp

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)



@app.route("/animelist")
def animelist():
    username = request.cookies.get('username')
    return render_template('animelist.html')

@app.route('/logout')
def logout():
    # Supprimer le cookie 'username' lors de la déconnexion
    resp = make_response(redirect('/logout-page'))  # Redirection vers la page de déconnexion
    resp.set_cookie('username', '', expires=0)  # Le cookie expire instantanément
    return resp 

@app.route('/logout-page')
def logout_page():
    return render_template('logout.html')


DATABASE = '/path/to/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()