from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm, CustomPasswordChangeForm


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('books:index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрированы!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile_user(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(profile_form.errors)
            print(password_form)
    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)
    context = {'profile_form': profile_form, 'password_form': password_form}
    return render(request, 'users/profile.html', context)


def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('books:index'))
