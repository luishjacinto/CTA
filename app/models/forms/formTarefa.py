# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import DateField,StringField, TextAreaField,PasswordField,Form,SubmitField,BooleanField,validators,IntegerField,SelectField
from wtforms.validators import DataRequired, InputRequired

class formTarefa(FlaskForm):
    style = {'class':'form-control'}
    
    nome=StringField("Nome",[
        validators.InputRequired(message="Campo obrigatorio"),validators.Length(min=3,max=60, message="O nome deve conter entre 3 e 60 caracteres")],render_kw=style)

    prioridade=SelectField(
        'Prioridade',coerce=int,
        choices=[(0, 'Muito Baixa'), (1, 'Baixa'), (2, 'Média'), (3, 'Alta'), (4, 'Muito Alta')],render_kw=style)

    status=SelectField(
        'Status',coerce=int,
        choices=[(0, 'Em desenvolvimento'), (1, 'Parado'), (2, 'Concluido')],render_kw=style)

    tipo=SelectField(
        'Tipo',coerce=int,
        choices=[(0, 'Documentação'), (1, 'Desenvolvimento'), (2, 'Produção'), (3, 'Outra')],render_kw=style)

    submit = SubmitField('Confirmar',render_kw={'class':'btn btn-primary'})