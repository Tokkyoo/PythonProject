import sqlite3
import datetime
from flask import Flask, render_template, request, make_response, redirect, g

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def valid_login(username, password):
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user
 

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
    query = '''
    SELECT Animes.name, Animes.description, Animes.episode_count, Watched_Animes.finish_date
    FROM Watched_Animes
    INNER JOIN Animes ON Watched_Animes.anime_id = Animes.id
    INNER JOIN Users ON Watched_Animes.user_id = Users.id
    WHERE Users.username = ?;
    '''
    watched_animes = query_db(query, [username], one=False)
    print(watched_animes)
    return watched_animes

def query_db(query, args=(), one=False):
    try:
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        print("Error executing query:", e)
        return None

@app.route("/animelist")
def animelist():
    username = request.cookies.get('username')
    
    print(username)
    if username:
        watched_animes = get_watched_animes(username)
        print('pipi')
        print(watched_animes)
        return render_template('animelist.html', watched_animes=watched_animes)
    else:
        return redirect('/login')



