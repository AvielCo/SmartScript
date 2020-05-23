import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, TextField
from flask_wtf import RecaptchaField
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
from config import *
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature, TimedSerializer
from re import compile
from functools import wraps
import string
import secrets
from flask_uploads import UploadSet, configure_uploads, IMAGES 
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.pymongo import ModelView
from predictFromWeb import runPredict
from random import randrange

app = Flask(__name__)
app.config['USER_APP_NAME'] = 'Hebrew Scripts Classifier'

# Recaptcha fields
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_SITE_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_SECRET_KEY
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
app.secret_key = APP_SECRET_KEY

# MongoDB fields
cluster = MongoClient("mongodb+srv://" + MONGO_USERNAME + ":" + MONGO_PASS + "@" + DOMAIN +"-gfohi.mongodb.net/test?retryWrites=true&w=majority")
db = cluster[MONGO_CLUSTER]
collection = db[MONGO_DB]

# collection.delete_many({})
# exit()

# Flask Admin
class UserForm(Form):
    name = TextField('Name')
    email = TextField('Email')
    username = TextField('Username')
    registeration_time = TextField('Registeration Time')
    admin = TextField('Admin?')

class UserView(ModelView):
    column_list = ('username', 'name', 'email', 'registeration_time', 'admin')
    form = UserForm
    def is_accessible(self):
        if 'logged_in' in session:
            isAdmin = collection.find_one({'username' : session['username']})['admin']
            if isAdmin:
                return True
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        flash("You are not authorized.", "danger")
        return redirect(url_for('index'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if 'logged_in' in session:
            isAdmin = collection.find_one({'username' : session['username']})['admin']
            if isAdmin:
                return True
        return False
    
    def inaccessible_callback(self, name, **kwargs):
        flash("You are not authorized.", "danger")
        return redirect(url_for('index'))

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(UserView(collection))

# Mail configuration
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_ASCII_ATTACHMENTS'] = MAIL_ASCII_ATTACHMENTS
app.config['USER_ENABLE_EMAIL'] = True
mail = Mail(app)
URL_SERIALYZER = URLSafeTimedSerializer(APP_SECRET_KEY)
TOKEN_SERIALIZER = TimedSerializer(APP_SECRET_KEY)

# images handle
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = IMAGES_PATH
configure_uploads(app, photos)


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=2, max=50)])
    USERNAME_REGEX = compile(r'^[a-zA-Z][a-zA-Z0-9]+$')
    username = StringField('Username', [
        validators.Length(min=4, max=25),
        validators.Regexp(regex=USERNAME_REGEX, message="Username must contain only letters and digits, starts with a letter.")])
    email = StringField('Email', [validators.Length(min=6, max=50), validators.email("Email address is not valid.")])
    PASSWORD_REGEX = compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,20}\Z')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match.'),
        validators.Regexp(regex=PASSWORD_REGEX, message="Password must contain at least one digit, one uppercase and one lowercase letters.")
        ])
    confirm = PasswordField('Confirm Password')
    recaptcha = RecaptchaField()

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=6, max=20), validators.DataRequired()])

class ResetPassForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=50), validators.email("Email address is not valid")])

class VerifyResetPassForm(Form):
    token = StringField('Token')
    PASSWORD_REGEX = compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,20}\Z')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match'),
        validators.Regexp(regex=PASSWORD_REGEX, message="Password must contain at least one digit, one uppercase and one lowercase letters")
        ])
    confirm = PasswordField('Confirm Password')
    recaptcha = RecaptchaField()

def isLogin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
    return wrap

def isNotLogin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            flash('A user is already logged in', 'warning')
            return redirect(url_for('index'))
    return wrap

@app.route('/register', methods=['GET', 'POST'])
@isNotLogin
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate(): # Method == POST means that the action has been redirected from the form and not from URL (GET method)
        username = form.username.data
        _id = username
        usernames = collection.find_one({"_id" : _id}) # Check if username is unique
        if usernames != None:
            flash("Username already exists", "danger")
            return render_template('register.html', form=form) # Return to the same registeration page

        email = form.email.data.lower()
        res = collection.find_one({"email" : email}) # Check if email is unique
        if res != None:
            flash("Email already exists", "danger")
            return render_template('register.html', form=form) # Return to the same registeration page
        
        name = form.name.data
        reg_time = datetime.now() # Registeration time
        confirmed = False # After registeration, the user must confirm himself via confirmation mail in his mailbox
        admin = False # Default

        password = sha256_crypt.encrypt(str(form.password.data)) # Encrypt the password with SHA_256
        sendVerificationMail(mailTo=email, username=username)
        collection.insert_one({"_id": _id, "name": name, "email": email, "username": username, "password": password, "registeration_time": reg_time, "confirmed": confirmed, "admin" : admin})
        flash("You are now registered, a verification mail sent to {}. Please check your inbox".format(email), "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form) # In case the form is not valid, or the request method is not POST

def sendVerificationMail(mailTo, username):
    token = URL_SERIALYZER.dumps(mailTo, salt=SALT_FOR_CONFIRM) # Make a unique token for the specific mail
    url = url_for('confirm_email', token=token, _external=True) # Make a unique URL with the token
    msg = Message(subject='Hebrew Scripts Classifier Verification Mail',
    recipients=[mailTo],
    html = verificationEmailHTML(url=url, username=username))
    mail.send(msg)

def verificationEmailHTML(url, username):
    html = """
        <html lang="en">
            <head>
                <title>Verify your email address</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
                <style>
                    .button {
                        background-color: #20B2AA;
                        border: none;
                        color: white;
                        padding: 16px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border-radius: 15px;
                    }
                </style>
            </head>
            <body>
                <div style="color:#708090" align="left">
                    <div>
                        <h1>
                            <b>Verify your email address</b>
                        </h1>
                    </div>
                    <br/>
                    <div>
                        <h3>
                            <b>Hey %s,
                            <br/>Thanks for signing up for Hebrew Scripts Classifier! We\'re excited to have you as an early user.<br/>
                            Before we get started, we just need to confirm that this is you.</b>
                            <br/><br/>
                            <div>
                                <a href="%s" class="button">
                                    Verify your email address
                                </a>
                            </div>
                            <br/>
                            <div>
                                <b>Thanks,
                                <br/>Hebrew Scripts Classifier Team.</b>
                            </div>
                        </h3>
                    </div>
                </div>
            </body>
        </html>
    """ % (username, url)
    return html

@app.route('/confirm_email/<token>') # A generic function that takes the token as a parameter
def confirm_email(token):
    try:
        email = URL_SERIALYZER.loads(token, salt=SALT_FOR_CONFIRM)
    except BadSignature:
        flash("User doesn't exist", "danger")
        return redirect(url_for('index'))
    res = collection.find_one({"email" : email})
    if res == None: # No email matched the email from the URL
        flash("User doesn't exist", "danger")
        return redirect(url_for('index'))
    res["confirmed"] = True
    collection.update({"email" : email}, res) # Update the record with the new data (the confirmed flag is True)
    flash("User verified! now you can login", "success")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@isNotLogin # That function requires that no user will be logged in at the same time (on the same client browser)
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data # Get Form Fields
        result = collection.find_one({"username": username}) # Get user by username
        if result != None:
            password = result['password']
            password_candidate = form.password.data # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                if bool(result['confirmed']) == False:
                    flash("Please verify your email before logging in", "warning")
                    return render_template('login.html')
                    
                # Passed the authentication
                session['attempts'] = 0
                session['username'] = username
                email = collection.find_one({"username" : username})['email']
                flash('A mail with a verification token has been sent to {}. Token is available for one minute'.format(email), 'success')
                twoFactorAuthenticationMail(mailTo=email, username=username) # Send 2FA mail for the login
                return render_template('loginVerification.html')
            else:
                error = 'Username or password do not match'
                return render_template('login.html', error=error, form=form)
        else:
            error = 'Username or password do not match'
            return render_template('login.html', error=error, form=form)
    return render_template('login.html', form=form)

def twoFactorHTML(username, token):
    html = """
        <html lang="en">
            <head>
                <title>Sign in token</title>
            </head>
            <body>
                <div style="color:#708090">
                    <h1>
                        <b>Sign in token</b>
                    </h1>
                    <br/>
                    <h3>
                        Hey %s,
                        <br/>
                        Thanks for signing in for Hebrew Scripts Classifier!
                        <br/>
                        Before we sign you in, we just need to confirm that this is you.
                        <br/>
                        <br/>
                        Your token is: <b>%s<b>
                        <br/>
                        Thanks,
                        <br/>Hebrew Scripts Classifier Team.
                    </h3>
                </div>
            </body>
        </html>
    """ % (username, token)
    return html

def twoFactorAuthenticationMail(mailTo, username, subj='Hebrew Scripts Classifier Sign in token'):
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(6)) # Generate 6 length token with letters and digits combined
    tokenSerialized = TOKEN_SERIALIZER.dumps(token)
    session['token'] = tokenSerialized # Save the serialized token on the session vars to compare it to the input from the user, within 60 seconds
    msg = Message(subject=subj,
    recipients=[mailTo],
    html = twoFactorHTML(token=token, username=username))
    mail.send(msg)

@app.route('/verify2FA', methods=['POST'])
def verify2FA():
    token = request.form['token']
    try:
        tokenSerialized = TOKEN_SERIALIZER.loads(session['token'], max_age=65)
    except SignatureExpired: # In case that more than 60 seconds passed from the first login authentication
        flash('Please log in again, token expired', 'danger')
        session.pop('token')
        session.pop('username')
        session['attempts'] = 0
        return redirect(url_for('login'))
    if token == tokenSerialized:
        session['logged_in'] = True
        flash('You are now logged in', 'success')
        session['attempts'] = 0
        return redirect(url_for('index'))

    if session['attempts'] >= 2: # More than 3 attempts
        flash('Please log in again, token expired', 'danger')
        session.pop('token')
        session.pop('username')
        session['attempts'] = 0
        return redirect(url_for('login'))
    
    # Under 3 attempts but the tokens are not equal case
    session['attempts'] += 1
    flash('Token is incorrect', 'danger')
    return render_template('loginVerification.html') 

@app.route('/profile')
@isLogin # Login required
def profile():
    username = session['username']
    res = collection.find_one({"username" : username}) # Get the details of the username from the session variable
    name = res['name']
    email = res['email']
    regTime = res['registeration_time'].strftime('%d/%m/%Y')
    admin = res['admin']
    return render_template("profile.html", name=name, username=username, email=email, regTime=regTime, admin=admin)


@app.route('/logout')
@isLogin # Login required
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# Reset password with 2FA method
@app.route('/resetPassword', methods=['GET', 'POST'])
def resetPassword():
    form = ResetPassForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data.lower()
        username = form.username.data
        res = collection.find_one({"username" : username, "email": email}) # Get the details of the user by his mail and username
        if res == None: # No record found
            flash("Username or Email are incorrect", "danger")
            return render_template('resetPassword.html', form=form)
        subj = 'Hebrew Scripts Classifier Reset Password token'
        twoFactorAuthenticationMail(mailTo=email, username=username, subj=subj)
        usernameSerialized = TOKEN_SERIALIZER.dumps(username)
        session['username'] = usernameSerialized
        session['resetAttempts'] = 0
        flash('A mail with a reset password token has been sent to {}. Token is available for one minute'.format(email), 'success')
        return redirect(url_for('verifyResetPass'))
    return render_template('resetPassword.html', form=form)

@app.route('/verifyResetPass', methods=['GET', 'POST'])
def verifyResetPass():
    form = VerifyResetPassForm(request.form)
    if request.method == 'POST' and form.validate():
        token = form.token.data
        password = sha256_crypt.encrypt(str(form.password.data))
        try:
            tokenSerialized = TOKEN_SERIALIZER.loads(session['token'], max_age=65)
        except SignatureExpired:
            flash('Token expired, please try again and insert token within 60 seconds', 'danger')
            session.pop('token')
            session['resetAttempts'] = 0
            return redirect(url_for('resetPassword'))
        if token == tokenSerialized:
            username = TOKEN_SERIALIZER.loads(session['username'], max_age=65)
            res = collection.find_one({"username" : username})
            res["password"] = password
            collection.update({"username" : username}, res)
            session.clear()
            session['resetAttempts'] = 0
            flash('Password changed successfully', 'success')
            return redirect(url_for('login'))

        if session['resetAttempts'] >= 2:
            flash('Too many attempts, please try again and insert the correct token', 'danger')
            session.clear()
            session['resetAttempts'] = 0
            return redirect(url_for('index'))
        
        session['resetAttempts'] += 1
        flash('Token is incorrect', 'danger')
        return render_template('verifyResetPass.html', form=form)
    return render_template('verifyResetPass.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
@isLogin
def upload():
    if request.method == 'POST' and 'image' in request.files:
        imageName = photos.save(request.files['image'])
        folderID = str(randrange(1000, 100000))
        if not os.path.exists(IMAGES_PATH):
            os.mkdir(IMAGES_PATH)
        os.mkdir(os.path.join(IMAGES_PATH, folderID)) # Make a folder with the generated folderID for each client
        os.replace(os.path.join(IMAGES_PATH, imageName), os.path.join(IMAGES_PATH, folderID, imageName)) # Move the image to its folder
        results = runPredict(folderID=folderID) # Run prediction on the folder, includes crop
        return render_template('upload.html', imageName=imageName, ashkenazi=results["ashkenazi"], notAshkenazi=results["notAshkenazi"])
    return render_template('upload.html', imageName="")


if __name__ == "__main__":
    app.run(host=HOST)