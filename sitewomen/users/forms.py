import datetime

from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    email = forms.EmailField(
        label="E-mail", widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    first_name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    last_name = forms.CharField(
        label="Фамилия", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    password2 = forms.CharField(
        label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Имя", max_length=255, widget=forms.TextInput(attrs={"class": "form-input"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-textarea", "cols": 60, "rows": 10})
    )
    captcha = CaptchaField()

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    email = forms.EmailField(
        disabled=True,
        required=False,
        label="E-mail",
        widget=forms.EmailInput(attrs={"class": "form-input"}),
    )
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        label="Дата рождения",
        widget=forms.SelectDateWidget(
            years=range(this_year - 100, this_year - 5), attrs={"class": "form-select"}
        ),
    )
    first_name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    last_name = forms.CharField(
        label="Фамилия", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    photo = forms.ImageField(
        label="Фото", required=False, widget=forms.ClearableFileInput(attrs={"class": "form-file-input"})
    )

    class Meta:
        model = get_user_model()
        fields = ["photo", "username", "email", "date_birth", "first_name", "last_name"]


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    new_password1 = forms.CharField(
        label="Новый пароль", widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
    )