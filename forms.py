from flask.ext.wtf import Form
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
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
			choices=[('tunnel', 'Tunnel'), ('transport','Transport')]
		)
	enc_alg = StringField("encryption algorithm")
	enc_key = StringField("encryption key")
	auth_alg = StringField("authentication algorithm")
	auth_key = StringField("authentication key")
    	submit = SubmitField('Submit')

class DelIpsecSaForm(Form):
	delete = SelectMultipleField('Label', [('1','1'),('2','2')])
