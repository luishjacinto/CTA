# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, Email, Length

class formBusca(FlaskForm):
    style = {'class':'form-control'}

    busca=StringField([
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(max=100,message="Esse campo pode ter no maximo 100 caracteres")],
        render_kw={
            'class' : 'form-control',
            'placeholder':'Insira sua busca'
        })

    submit = SubmitField('Buscar',render_kw={'class':'btn btn-primary'})
