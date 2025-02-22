from fasthtml.common import *
from dataclasses import dataclass
import pages
import bcrypt
from verifyEmail import verifyEmail

# Form dataclass, basically the object that is used as standard for the database
@dataclass
class User: email:str; password:str;

profile_form = Form(method="post")  (
        Fieldset(
            Label('Email', Input(name="email")),
            Label("Password", Input(name="password", type="password")),
        ),
        Button("Register", type="submit"),
    )
login_form = Form(method="post")(
    Fieldset(
        Label("Email", Input(name="email")),
        Label("Password", Input(name="password", type="password"))
    ),
    Button("Login", type="submit"),
)

# Database
db = database("users.db")
users = db.create(User, pk="email")

# User register handling
def register_user(email: str, password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    print(hashed_password)
    user = User(email,hashed_password)
    users.insert(user)

def fetch_user(email: str, input_password: str):
    if not email in users:
        return -2

    user = users[email] # Email is the primary key

    result = bcrypt.checkpw(input_password.encode(), user.password) # Verifies if password is correct

    if result == False:
        return -1 # User exists but wrong password
    
    return user

# User authentication
login_redirect = RedirectResponse('/login', status_code=303)

# Checks if the user is authenticated by checking the session information
def user_auth_before(request, session):
    auth = request.scope['auth'] = session.get('auth', None)
    if not auth: return login_redirect

# Runs right before changing pages
beforeware = Beforeware(
    user_auth_before,
    skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', r'.*\.js', '/login', '/', '/about', '/register']
)

headers = (Link(rel="stylesheet", href="assets/css/style.css"),)

# FastAPI app
app, rt = fast_app(debug=True, before=beforeware, hdrs=headers)

@app.get("/")
def home():
    return pages.home

@app.post("/")
def post(request, session):
    user_auth_before(request, session)
    print(session["auth"]) # Use this for authentication
    return pages.home

@rt("/register")
def get():
    return Titled("Faça seu cadastro", profile_form)

@rt("/login")
def get():
    return Titled(f"Faça seu login", login_form)

# Receives the login information and sets the auth variable in the session
@app.route("/login", methods=['post'])
def post(email: str, password: str, session):
    user = fetch_user(email, password)
    if user == -1:
        return Titled("Wrong Password")
    if user == -2:
        return Titled("This e-mail is not yet registered")

    session.setdefault("auth",email)
    return Titled()


@rt("/profile")
def get(session):
    email, p = session.get("auth")

    return Titled(f"{email}'s Profile")

# Receives the register information and creates an entry in the database
@app.route("/register", methods=['post'])
def post(email: str, password: str): # Variable position must match form input index
    
    #Verify if e-mail is from Etec's domain
    emailVerifier = verifyEmail(email)
    if(emailVerifier):
        pass
    else:
        return Titled("This e-mail is not from Etec, please use your Etec's e-mail")
    
    user = fetch_user(email, password)
    if user != -2: # User DOES exist
        return Titled("This e-mail has already been registered")

    print(f"email: {email}\npassword: {password}\n")
    register_user(email, password)
     
    return home() # Go to home page

@rt("/about")
def get():
    return Titled("Who we are", P("Lorem ipsum dolor sit amet"))

serve()