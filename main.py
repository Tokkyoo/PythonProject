import sqlite3
import datetime
from flask import Flask, render_template, request, make_response, redirect, g, url_for

from pathlib import Path
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


def valid_login(username, password):
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    return user

def already_register(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user is not None

def log_the_user_in(username):
    # Cette fonction pourrait enregistrer l'utilisateur connecté dans une session ou effectuer d'autres actions.
    resp = make_response(redirect('/animelist'))
    resp.set_cookie('username', username)#Je mets comme value l'utisateur que j'ai mis en parametre, en effet c'est pas sécurisé.
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


@app.route('/logout')
def logout():
    # Supprimer le cookie 'username' lors de la déconnexion
    resp = make_response(redirect('/logout-page'))  # Redirection vers la page de déconnexion
    resp.set_cookie('username', '', expires=0)  # Le cookie expire instantanément
    return resp 

@app.route('/logout-page')  
def logout_page():
    return render_template('logout.html')


DATABASE = 'database.db'

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


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('animelist.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_watched_animes(username):
    # Exécuter la requête SQL pour récupérer les animés regardés par l'utilisateur
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT Animes.name, Animes.description, Animes.episode_count, Watched_Animes.finish_date
    FROM Watched_Animes
    INNER JOIN Animes ON Watched_Animes.anime_id = Animes.id
    INNER JOIN Users ON Watched_Animes.user_id = Users.id
    WHERE Users.username = ?;
    ''', (username,))
    watched_animes = cursor.fetchall()
    conn.close()
   
    print(watched_animes)
    return watched_animes


@app.route("/animelist")
def animelist():
    username = request.cookies.get('username')
    
    print(username)
    if username:
        watched_animes = get_watched_animes(username)
        
        print(watched_animes)
        return render_template('animelist.html', watched_animes=watched_animes)
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # Traitement du formulaire d'inscription ici
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur est déjà enregistré
        if already_register(username):
            error = 'Username already exists. Please choose a different username.'
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            db.commit()  # Commit the transaction before closing the connection
            return redirect(url_for('login'))

    # Si la méthode de requête est GET ou si une erreur s'est produite, afficher la page d'inscription
    return render_template('register.html', error=error)

if not Path(DATABASE).exists():
    with app.app_context():
        db = get_db()
        sql = Path('ideas.sql').read_text()
        db.cursor().executescript(sql)
        db.commit()