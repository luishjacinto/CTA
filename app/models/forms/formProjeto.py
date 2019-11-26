# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import DateField,StringField, TextAreaField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.validators import DataRequired, InputRequired

class formProjeto(FlaskForm):
    style = {'class':'form-control'}
    text = {'class':'form-control',
        'rows':'10',
        'col':'20'
    }
    
    nome=StringField("Nome",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(min=3,max=200,message="O nome deve ter entre 3 e 200 caracteres")],render_kw=style)

    descricao=TextAreaField("Descricao",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(min=10,max=3000,message="Este campo deve ter entre 10 e 3000 caracteres")],render_kw=text)

    status=SelectField(
        'Status',coerce=int,
        choices=[(0, 'Em desenvolvimento'), (1, 'Parado'), (2, 'Concluido')],render_kw=style)

    submit = SubmitField('Confirmar',render_kw={'class':'btn btn-primary'})