from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, RegistrationForm


def login_view(request):
    # Kept for compatibility but login uses Django's built-in LoginView
    return render(request, 'accounts/login.html')


def register_view(request):
    """Show registration form and on success redirect to login page.

    If user is already authenticated redirect to products home.
    """
    if request.user.is_authenticated:
        return redirect('products:product_list')

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login the user after successful registration
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful. You are now logged in.')
                return redirect('products:product_list')
            messages.error(request, 'Registration saved but could not log you in. Please login.')
            return redirect('accounts:login')
        else:
            # show form errors
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'accounts/register.html', {'form': form})


def profile_view(request):
    # Show basic user info
    return render(request, 'accounts/profile.html', {'user_obj': request.user})


def logout_view(request):
    """Log the user out and redirect to the register page.

    Security: only accept POST to avoid CSRF via GET links.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:register')


@login_required
def profile_edit(request):
    """Allow the user to edit first name, last name and email."""
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name') or ''
            user.last_name = form.cleaned_data.get('last_name') or ''
            user.email = form.cleaned_data.get('email') or ''
            user.save()
            return redirect('accounts:profile')
    else:
        form = ProfileForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })

    return render(request, 'accounts/profile_edit.html', {'form': form})
