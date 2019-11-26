# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import DateField,StringField, FileField, TextAreaField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.validators import DataRequired, InputRequired

class formFoto(FlaskForm):

    text = {'class':'form-control',
        'rows':'10',
        'col':'20'
    }

    descricao=TextAreaField("Descrição",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(min=3,max=1000,message="Este campo deve conter entre 3 e 1000 caracteres")],render_kw=text)

    foto=FileField('Foto')


    submit = SubmitField('Confirmar',render_kw={'class':'btn btn-primary'})