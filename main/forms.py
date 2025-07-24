from .models import Joke
from django.forms import ModelForm, TextInput, Textarea

class JokeForm(ModelForm):
    class Meta:
        model = Joke
        fields = ['title', 'joke']
        widgets = {'title': TextInput(attrs = {
            'class': "form-control", 'placeholder': 'Заголовок'
            }), 'joke': Textarea(attrs = {
            'class': "form-control", 'placeholder': 'Рассказывайте анекдот'
            })
        }