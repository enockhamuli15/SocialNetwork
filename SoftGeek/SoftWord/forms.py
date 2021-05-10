from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class LoginForm(UserCreationForm):

    class Meta:
        model = Logins
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class PostForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ('description', 'image_attached', 'domain')
        widgets = {
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'4'}),
            'domain': forms.Select(attrs={'class':'form-control form-control-sm'})

        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['domain'].empty_label = Domains.objects.get(id=1)


    
class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={
                                'placeholder': 'Leave a comment...', 
                                'class':'form-control form-control sm',
                                }))
    class Meta:
        model = Comment
        fields = ('body',)
