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
        fields = ['full_name', 'email', 'phone_number']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name'   : forms.TextInput(attrs={'class': 'form-control'}),
            'email'       : forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'true'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control',}),
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
        widgets = {
            'date_of_birth'  : forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'sex'            : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sex'}),
            'road'           : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Road'}),
            'ward'           : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ward'}),
            'district'       : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
            'city'           : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'bio'            : forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio'}),
        }

        # def clean(self):
        #     cleaned_data = super(UserProfileForm, self).clean()
        #     old_password = cleaned_data.get('old_password')
        #     new_password = cleaned_data.get('new_password')
        #     confirm_password = cleaned_data.get('confirm_password')
        #
        #     if new_password != confirm_password:
        #         raise forms.ValidationError('New password does not match!')
        #
        #     return cleaned_data


        









