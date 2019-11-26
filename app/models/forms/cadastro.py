# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired

class formCadastro(FlaskForm):
    style = {'class':'form-control'}

    nome=StringField("Nome",[
        validators.InputRequired(message="Campo obrigatorio"), validators.Length(min=3,max=60,message="O nome deve conter entre 3 e 60 caracteres")],render_kw=style)
    
    email=StringField("Email",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(max=100, message="O email pode conter no maximo 100 caracteres"),validators.Email(message="Insira um Email válido")],render_kw=style)

    senha=PasswordField("Senha",[
        validators.InputRequired(message="Campo obrigatorio"),
        validators.Length(min=3,max=50,message="A senha deve conter 3 e 50 caracteres")],render_kw=style)

    data=DateField("Data nascimento",[
        validators.InputRequired(message="Campo obrigatorio")],render_kw=style)

    submit = SubmitField('Cadastrar',render_kw={'class':'btn btn-primary'})
