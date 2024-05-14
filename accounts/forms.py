from django import forms
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = Account
        fields = ['full_name', 'email', 'phone_number', 'password', 'confirm_password']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password: 
            raise forms.ValidationError('Password does not match!')

        return cleaned_data 


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['full_name', 'username', 'email', 'phone_number']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'name': 'user_name', 'placeholder': 'Username'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control','name': 'full_name', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'true'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'name': 'phone', 'placeholder': 'Phone'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'sex', 'road', 'ward', 'district', 'city', 'bio', 'profile_picture']
