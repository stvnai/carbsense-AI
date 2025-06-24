from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class InputForm(FlaskForm):
    
    tss= IntegerField(
        "TSS",
        validators= [
            DataRequired(),
            NumberRange(min=5, max=800)
        ],
            render_kw={"placeholder": 200})
    
    int_factor= DecimalField(
        "IF",
        validators= [
            DataRequired(),
            NumberRange(min=0.01, max=1.0)
        ],
            render_kw={"placeholder": 0.75})
    
    kcal= IntegerField(
        "kcal", 
        validators= [
            DataRequired(), 
            NumberRange(min=25, max= 7000)
        ],
            render_kw={"placeholder": 2000})
    
    weight= DecimalField(
        "weight", 
        validators= [
            DataRequired(), NumberRange(min= 50, max=250)
        ],
            render_kw={"placeholder": 65})
    
    submit= SubmitField("Calculate")


