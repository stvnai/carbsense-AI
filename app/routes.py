import os
import joblib
import numpy as np
from app.forms import InputForm, LoginForm, SignupForm
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.auth.controller import authenticate_user
from app.decorators.auth_decorators import login_required
from werkzeug.security import generate_password_hash

model_path= os.path.join(os.path.dirname(__file__), "model", "cho-estimator.pkl" )

model= joblib.load(model_path)

main= Blueprint("main", __name__)

### LOGIN ###

@main.route("/login", methods=["GET", "POST"])
def login():
    login_form= LoginForm()

    if login_form.validate_on_submit():

        username= login_form.username.data
        password= login_form.password.data

        user_id= authenticate_user(username, password)
        if user_id:
            session["user_id"] = user_id
            return redirect(url_for("main.index"))
        
        else:
            flash("Wrong username or password", "danger")
            return redirect(url_for("main.login"))

    return render_template("login.html", login_form=LoginForm())

### SIGN UP ###

@main.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form= SignupForm()

    if signup_form.validate_on_submit():

        email= signup_form.email.data
        username= signup_form.username.data
        password= signup_form.password.data

        password_hashed= generate_password_hash(password)

        

    return render_template("login.html", login_form=LoginForm())

### MAIN FORM ###

@main.route("/", methods=["GET", "POST"])
@login_required
def index():

    form= InputForm()

    if form.validate_on_submit():

        tss= form.tss.data
        int_factor= form.int_factor.data
        kcal= form.kcal.data
        weight= form.weight.data
        sex_toggle= request.form.get("sex")
        units_toggle= request.form.get("unit")

        int_factor = int(int_factor > 0.65)
        
        sex= 0 if sex_toggle == "on" else 1

        if units_toggle == "on":
            weight= float(weight)
            weight/=2.205

        features= np.array([tss, kcal, weight, int_factor, sex]).reshape(1,-1)

        prediction= max(0,model.predict(features)[0])
        session["prediction"] = f"{prediction:.2f}"
        return redirect(url_for("main.results"))

    return render_template("index.html", form= form)

### RESULTS ###

@main.route("/results", methods=["GET"])
@login_required
def results():
    prediction= session.pop("prediction", None)
    
    if prediction is None:
        return redirect(url_for("main.index"))
    
    return render_template("results.html", prediction = prediction) 

### LOGOUT ###

@main.route("/logout")
@login_required


def logout():
    """Close session and redirect to /login"""

    session.pop("user_id", None)
    return redirect(url_for("main.login"))


