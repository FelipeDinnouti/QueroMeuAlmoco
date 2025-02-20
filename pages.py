from fasthtml.common import *

submit_button = Form(method="post")(
    Button("Quero Almoço", type="submit", id="center_button"),
    style="text-align: center"
)

home = Div(
    H1(
        "Quero Meu Almosso!!",
        id="main_title"
    ),
    A("Register", href = "/register"), Br(), A("Login", href="/login"), Br(), A("Profile", href="/profile"),
    submit_button,
    cls="container"
)