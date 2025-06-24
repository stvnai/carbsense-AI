import os
import joblib
import numpy as np
from app.forms import InputForm
from flask import Blueprint, render_template, request

model_path= os.path.join(os.path.dirname(__file__), "model", "cho-estimator.pkl" )

model= joblib.load(model_path)

main= Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
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
        return render_template("results.html", prediction= f"{prediction:.2f}")

    return render_template("index.html", form= form)
