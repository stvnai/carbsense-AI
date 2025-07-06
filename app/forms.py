from flask_wtf import FlaskForm
import re
from wtforms import IntegerField, DecimalField, SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Length, Email, ValidationError

def validate_username(form, field):
    if not re.match(r"^[a-zA-ZA0-9_.-]+$",field.data):
        raise ValidationError("Only letters, numbers, '-', '_' or '.' are allowed.")


# Data fields
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

# Login

class LoginForm(FlaskForm):
    username= StringField(
        "username",
        validators= [
            InputRequired(),
            Length(max=150),
            validate_username
        ]
    )
            

    password= PasswordField(
        "password",
        validators= [
            InputRequired(),
            Length(max=50)
        ]
    )

    submit_user= SubmitField("Sign In")

# Sign Up

class SignupForm(FlaskForm):
    email= EmailField(
        "email",
        validators= [
            InputRequired(),
            Email(message="Invalid mail format."),
            Length(max= 255)
        ]
    )
    
    username= StringField(
        "username",
        validators= [
            InputRequired(),
            Length(min=8, max=150)
        ]
    )

    password= PasswordField(
        "password",
        validators=[
            InputRequired(),
            Length(min=8, max=50)
        ]
    )


