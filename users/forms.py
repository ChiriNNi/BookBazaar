from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm


from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", max_length=100, widget=forms.TextInput(attrs={
        'class': 'input100',
        'placeholder': 'Username'
    }))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        'class': 'input100',
        'placeholder': 'Password'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={
        'class': 'input100',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={
        'class': 'input100',
        'placeholder': 'Last Name'
    }))
    username = forms.CharField(label="Логин", max_length=100, widget=forms.TextInput(attrs={
        'class': 'input100',
        'placeholder': 'Username'
    }))
    email = forms.CharField(label="Электронная почта", max_length=100, widget=forms.EmailInput(attrs={
        'class': 'input100',
        'placeholder': 'Email'
    }))
    password1 = forms.CharField(label="Пароль", max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'input100',
        'placeholder': 'Password'
    }))
    password2 = forms.CharField(label="Подтверждение пароля", max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'input100',
        'placeholder': 'Confirm the password'
    }))
    profile_type = forms.ChoiceField(choices=User.PROFILE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'profile_type')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Электронная почта", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Изображение', widget=forms.FileInput(attrs={'hidden': 'hidden'}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'image')


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))