from fasthtml.common import *
from dataclasses import dataclass
import pages

# Form dataclass, basically the object that is used as standard for the database
@dataclass
class User: email:str; password:str; gender:bool; # 0 (False) is male, 1 is female 

profile_form = Form(method="post")  (
        Fieldset(
            Label('Email', Input(name="email")),
            Label("Password", Input(name="password", type="password")),
            Label("Gender", Input(name="gender", type = "checkbox")),
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
def register_user(email: str, password: str, gender: bool):
    user = User(email, password, gender)
    users.insert(user)

def fetch_user(email: str, password: str):
    if not email in users:
        return -2

    user = users[email] # Email is the primary key

    if user.password != password: # Very secure password
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
    return Titled(f"Gender: {user.gender}")


@rt("/profile")
def get(session):
    email, p = session.get("auth")

    return Titled(f"{email}'s Profile")

# Receives the register information and creates an entry in the database
@app.route("/register", methods=['post'])
def post(email: str, password: str, gender: bool): # Variable position must match form input index
    user = fetch_user(email, password)
    if user != -2: # User DOES exist
        return Titled("This e-mail has already been registered")

    print(f"email: {email}\npassword: {password}\ngender: {gender}")
    register_user(email, password, gender)
     
    return home() # Go to home page

@rt("/about")
def get():
    return Titled("Who we are", P("Lorem ipsum dolor sit amet"))

serve()