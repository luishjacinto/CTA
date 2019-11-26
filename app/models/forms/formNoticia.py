# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import DateField,StringField, TextAreaField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.validators import DataRequired, InputRequired

class formNoticia(FlaskForm):
    style = {'class':'form-control'}
    text = {'class':'form-control',
        'rows':'10',
        'col':'20'
    }
    
    nome=StringField("Nome",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(min=3,max=200,message="O nome deve ter entre 3 e 200 caracteres")],render_kw=style)

    conteudo=TextAreaField("Conteúdo",[validators.InputRequired(message="Campo obrigatorio"),validators.Length(min=3,max=10000,message="Este campo deve ter entre 3 e 10000 caracteres")],render_kw=text)

    submit = SubmitField('Confirmar',render_kw={'class':'btn btn-primary'})