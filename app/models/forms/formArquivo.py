# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import DateField,StringField, FileField, TextAreaField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.validators import DataRequired, InputRequired

class formArquivo(FlaskForm):
    style = {'class':'form-control'}

    nome=StringField("Nome",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(min=1,max=96,message="O nome deve conter entre 1 e 96 caracteres")],render_kw=style)

    arquivo=FileField('Arquivo')


    submit = SubmitField('Confirmar',render_kw={'class':'btn btn-primary'})