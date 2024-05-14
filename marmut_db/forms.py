from django import forms
from .models import Akun, Label, Songwriter, Artist, Podcaster

from django import forms
from django.contrib.auth.hashers import make_password
from .models import Akun, Podcaster, Artist, Songwriter

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password'}))
    gender = forms.ChoiceField(choices=[(0, 'Female'), (1, 'Male')], widget=forms.Select(attrs={'class': 'form-control', 'id': 'gender'}))
    role = forms.MultipleChoiceField(
        choices=[('podcaster', 'Podcaster'), ('artist', 'Artist'), ('songwriter', 'Songwriter')],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    tanggal_lahir = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'birthdate'}))

    class Meta:
        model = Akun
        fields = ['email', 'password', 'nama', 'gender', 'tempat_lahir', 'tanggal_lahir', 'kota_asal']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'nama': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'tempat_lahir': forms.TextInput(attrs={'class': 'form-control', 'id': 'birthplace'}),
            'kota_asal': forms.TextInput(attrs={'class': 'form-control', 'id': 'city'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])

        roles = self.cleaned_data.get('role', [])
        if roles:
            user.is_verified = True
        else:
            user.is_verified = False

        if commit:
            user.save()
            for role in roles:
                if role == 'podcaster':
                    Podcaster.objects.create(email=user)
                elif role == 'artist':
                    Artist.objects.create(email_akun=user)
                elif role == 'songwriter':
                    Songwriter.objects.create(email_akun=user)
        return user


class LabelRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Label
        fields = ['email', 'password', 'nama', 'kontak']
