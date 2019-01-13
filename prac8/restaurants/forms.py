from django import forms
from django.contrib.auth.models import User

from .models import Dish

class LoginForm(forms.Form):
    login_username = forms.SlugField (max_length=8, label='Usuario: ')
    login_password = forms.SlugField (max_length=8, widget=forms.PasswordInput(),label='Contraseña:',help_text='Hasta 8 letras')
    
    class Meta:
        model  = User
        fields = ('login_username',  'login_password')

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ('name', 'type_cousine', 'allergens', 'price')
