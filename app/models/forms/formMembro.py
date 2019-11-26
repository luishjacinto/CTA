# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Email, Length

class formMembro(FlaskForm):
    style = {'class':'form-control'}

    email=StringField("Email",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(max=100,message="Esse campo pode ter no maximo 100 caracteres"),
        validators.Email(message="Insira um Email válido")],render_kw=style)

    submit = SubmitField('Confirmar',render_kw={'class':'btn btn-primary'})
