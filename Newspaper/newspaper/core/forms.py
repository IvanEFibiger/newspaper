from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 

    class Meta(UserCreationForm.Meta):
        model = User  
        fields = ('username', 'email', 'password1', 'password2')





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Solo necesitas el contenido del comentario
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu comentario...'}),
        }