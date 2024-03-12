from flask import Flask, render_template, request

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
    return f'Logged in as {username}'

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

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.


@app.route("/animelist")
def animelist():
    return render_template('animelist.html')