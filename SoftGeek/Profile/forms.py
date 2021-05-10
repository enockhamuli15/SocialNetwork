from django import forms
from .models import Profile
from SoftWord.models import Logins
from django.contrib.auth.forms import UserCreationForm

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Logins
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'last_name': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'username': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'email': forms.TextInput(attrs={'class':'form-control form-control-sm'})
        }


class ProfileUpdateForm(forms.ModelForm):

    dateOfBirth = forms.DateInput()
    class Meta:
        model = Profile
        
        fields = ['description', 'dateOfBirth', 'phoneNum','profile_photo']
        widgets = {
            'description': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3'}),
            'dateOfBirth': forms.TextInput(attrs={'class':'form-control form-control-sm'}),
            'phoneNum': forms.TextInput(attrs={'class':'form-control form-control-sm'})
        }
