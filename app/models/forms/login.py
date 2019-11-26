# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import DateField,StringField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.validators import DataRequired, InputRequired

class formLogin(FlaskForm):
    style = {'class':'form-control'}
    
    email=StringField("Email",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(max=100, message="O email pode conter no maximo 100 caracteres"),
        validators.Email(message="Insira um Email válido")],render_kw=style)

    senha=PasswordField("Senha",[
        validators.InputRequired(message="Campo obrigatorio"),
        validators.Length(min=3,max=50,message="A senha deve ter entre 3 e 50 caracteres")],render_kw=style)

    submit = SubmitField('Entrar',render_kw={'class':'btn btn-primary'})
