from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm ,UsernameField, PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _

class SignUpForm(UserCreationForm):  #inherits the default form to create extra fields
    password1 = forms.CharField(label= 'Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your Password'}))
    password2 = forms.CharField(label= 'Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter your Confirm Password'}))  #overridding this field
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'first_name':'First_Name', 'last_name':'Last_Name', 'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Username'}),
        'first_name':forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your First Name'}),
        'last_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Last Name'}),
        'email':forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your Email Id'})
        } 

class ContactForm(forms.Form):
    Name = forms.CharField(label='',widget=forms.TextInput
                           (attrs={'placeholder':'Enter Your Name', 'class': 'form-control'}))
    Email = forms.EmailField(max_length=50, label='', widget=forms.TextInput
                           (attrs={'placeholder':'Enter Your Email Id', 'class': 'form-control'}))
    Mobile = forms.CharField(max_length=10,label='', widget=forms.TextInput
                           (attrs={'placeholder':'(xxx)xxx-xxxx', 'class': 'form-control'}))
    Message = forms.CharField(label='', widget=forms.Textarea
                           (attrs={'placeholder': 'Enter your comment here', 'class': 'form-control', 'rows':3}))

def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        Name = cleaned_data.get('Name')
        Email = cleaned_data.get('Email')
        Mobile = cleaned_data.get('Mobile')
        Message = cleaned_data.get('Message')
        if not Name and not Email and not Message and not Mobile:
            raise forms.ValidationError('Fill the fields')
        

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control','placeholder':'Enter Username'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control', 'placeholder':'Enter Password'}),
    )

# class UserLogin(AuthenticationForm):
#     widgets={'username':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter your Username'}),
#     'password':forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your Password'})
#     }

