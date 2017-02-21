from flask_wtf import Form
from datetime import datetime
from wtforms import TextAreaField, TextField, validators
from wtforms_components import EmailField
from wtforms_components import SelectField
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from wtforms_components import DateTimeField
from wtforms.validators import DataRequired, Length


class ContactForm(Form):
	email = EmailField("Email",
                       [DataRequired(), Length(3, 254)])
	projectid = TextField("Project Name",
                       [DataRequired(), Length(3, 254)])
	description = TextAreaField("Description",
                            [DataRequired(), Length(1, 2000)])
#	skills = TextAreaField("Extra Curricular Activity",
#                            [DataRequired(), Length(1, 2000)])
	skills = TextAreaField("Extra Curricular Activity",
                            [Length(1, 2000)])

   	department = SelectField(u'School', choices=[
        ('Donlon','Donlon Elementary'),('Mohr','Mohr Elementary'),('Fairlands','Fairlands Elementary'),('Hearst','Hearst Elementary')
        ,('Stratford','Stratford Elementary'),('Hart','Thomas Hart Middle School'),('Harvest','Harvest Park Middle School')])
   	protype = SelectField(u'Grade', choices=[('kinder','Kinder Garten'),('first','First'),
        ('second','Second'),
        ('third','Third'),('fourth','Fourth'),
        ('fifth','Fifth'),('sixth','Sixth'),
        ('seventh','Seventh')])
	startdate = DateField('DatePicker', format='%Y-%m-%d')
	enddate = DateField('DatePicker', format='%Y-%m-%d')