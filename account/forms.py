from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login


class AddNewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","email","password1","password2")

    def __init__(self, *args, **kwargs):
        super(AddNewUser, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean(self):
        cleaned_data = super(AddNewUser, self).clean()
        email = cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exists():
                 raise ValidationError("User with this email address is already exist.")
        else:
            raise ValidationError("Please add email address")
        return self.cleaned_data

class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(UpdateUser, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean(self):
        cleaned_data = super(UpdateUser, self).clean()
        email = cleaned_data.get('email')
        if email:
            if User.objects.filter(email=email).exclude(email=self.instance.email).exists():
                raise ValidationError("User with this email address is already exist.")
        else:
            raise ValidationError("Please add email address")
        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field_name

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            if not User.objects.filter(Q(email=username) | Q(username=username)).exists():
                raise ValidationError("User does not exist with this username")
            
            user = User.objects.get(Q(email=username) | Q(username=username))
            if not user.check_password(password):
                raise ValidationError("Invalid password for this username.")
            if not user.is_active:
                raise ValidationError("User is not active.")
            self.user = user
            login(self.request, user)
        return self.cleaned_data
