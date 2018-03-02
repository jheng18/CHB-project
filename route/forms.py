from django import forms
from .model import get

MODE = [
    ('walk', 'Walk'),
    ('bike', 'Bike'),
    ('transit', 'Transit'),
    ]

TIME = [
    ('1-3', '1am-3am'),
    ('3-5', '3am-5am'),
    ('5-7', '5am-7am'),
    ('7-9', '7am-9am'),
    ('9-11', '9am-11am'),
    ('11-1', '11am-1pm'),
    ('1-3', '1pm-3pm'),
    ('3-5', '3pm-5pm'),
    ('5-7', '5pm-7pm'),
    ('7-9', '7pm-9pm'),
    ('9-11', '9pm-11pm'),
    ('11-1', '11pm-1am'),
    ]

class ODForm(forms.Form):
    Origin = forms.CharField(label='orgin', max_length=100)
    Destin = forms.CharField(label='destination', max_length=100)
