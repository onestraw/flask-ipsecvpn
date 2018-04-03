# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Required


class AddIpsecSaForm(Form):
    saddr = StringField("source addresss", validators=[Required()])
    daddr = StringField("destination addresss", validators=[Required()])
    spi = StringField("spi")
    proto = SelectField(
            "protocol",
            choices=[('esp', 'ESP'), ('ah', 'AH')]
        )
    mode = SelectField(
            "mode",
            choices=[('tunnel', 'Tunnel'), ('transport', 'Transport')]
        )
    enc_alg = StringField("encryption algorithm")
    enc_key = StringField("encryption key")
    auth_alg = StringField("authentication algorithm")
    auth_key = StringField("authentication key")
    submit = SubmitField('Submit')


class AddIpsecSpForm(Form):
    saddr = StringField("source addresss", validators=[Required()])
    daddr = StringField("destination addresss", validators=[Required()])
    direction = StringField("direction")
    proto = SelectField(
            "protocol",
            choices=[('esp', 'ESP'), ('ah', 'AH')]
        )
    mode = SelectField(
            "mode",
            choices=[('tunnel', 'Tunnel'), ('transport', 'Transport')]
        )
    priority = StringField("priority")
    sel_src = StringField("selector src")
    sel_dst = StringField("selector dst")
    submit = SubmitField('Submit')
