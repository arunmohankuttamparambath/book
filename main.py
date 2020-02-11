from flask import Flask, render_template, request, redirect, url_for, session
import service as dbHandler
import re

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'


""" @app.route('/', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        dbHandler.insertUser(username, password)
        users = dbHandler.retrieveUsers()
        return render_template('index.html', users=users)
    else:
        return render_template('index.html')
"""
@app.route('/', methods=['GET', 'POST'])
# http://localhost:5000/python/login - this will be the login page
@app.route('/python/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using sqlite3
        account = dbHandler.retrieveUsers(username, password)
        if account:
            #Create session data, we can access this data in other routes
            session['loggedin'] = True    
            session['id'] = account[0]
            session['username'] = account[5]
            #Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)        

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/python/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        account = dbHandler.retrieveId(session['id'])
        return render_template('home.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/python/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fs_name  = request.form['fs_name']
        ls_name = request.form['ls_name']
        su_name = request.form['su_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        account = dbHandler.retrieveUsers(username, password)
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            dbHandler.register(fs_name,ls_name,su_name,email,username,password)
            msg = 'You have successfully registered!'
            return "User Successfully Added !! Welcome " +fs_name +" " +ls_name +" " +su_name

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)    


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/python/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        uids = session['id'] 
        account = dbHandler.retrieveId(uids)
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)        