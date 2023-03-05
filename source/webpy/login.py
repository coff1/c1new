from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

login_bp = Blueprint('login', __name__)
login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

users = {
    1: User(1, "admin", "123")
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Find the user in the users dictionary
        user = next((user for user in users.values() if user.name == username), None)

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("index"))
        else:
            return render_template('login.html',i=1)
    return render_template('login.html',i=0)

@login_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("/"))
