# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import DateField,StringField, TextAreaField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired

class formRepo(FlaskForm):
    style = {'class':'form-control'}

    link=StringField("Link",[
        validators.InputRequired(message="Campo obrigatorio"), validators.Length(min=3,max=500,message="O link deve conter entre 3 e 500 caracteres")],render_kw=style)
    
    nome=StringField("Nome",[
        validators.InputRequired(message="Campo obrigatorio"), validators.Length(min=3,max=100,message="O nome deve conter entre 3 e 100 caracteres")],render_kw=style)

    submit = SubmitField('Confirmar',render_kw={'class':'btn btn-primary'})