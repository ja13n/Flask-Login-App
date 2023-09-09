from flask import Flask, render_template, redirect, url_for, flash
from Forms import MyForm, NewAccount
from Models import  User, db
from flask_login import LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "it's a secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loginpage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
app.app_context().push()
lm = LoginManager()
lm.init_app(app)


@app.route('/createaccount', methods=["GET", "POST"])
def createaccountpage():
    form = NewAccount()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirmed_password = form.confirm_password.data
        user = User(username=username)
        if password != confirmed_password:
            flash("The passwords did not match please try again")
            return redirect(url_for("createaccountpage", my_form=form))
        elif User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose a different username.")
            return redirect(url_for("createaccountpage", my_form=form))
        else: 
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Account created successfully!")
            return redirect(url_for("welcome", username=username))
    return render_template("createaccount.html", my_form=form)

@app.route("/login_page", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def login_page():
    form = MyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("welcome", username=user.username))
        else:
            flash("Invalid username or password.")
    return render_template("login.html", my_form=form)

@app.route("/welcome/<username>")
@login_required
def welcome(username):
    return render_template("welcome.html", username=username)

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/logout")
@login_required
def logout_page():
    form = MyForm()
    logout_user()
    return redirect(url_for("login_page", my_form=form))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
