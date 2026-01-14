from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def home(request):
    return render(request, 'base.html')


def landing(request):
    """Landing page: show login and register side-by-side for anonymous users.

    If user is authenticated, redirect to the products list.
    Handles POST for either login (name="login") or register (name="register").
    """
    if request.user.is_authenticated:
        return redirect('products:product_list')

    login_form = AuthenticationForm()
    register_form = UserCreationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('products:product_list')
        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                # log the user in after registering
                auth_user = authenticate(username=user.username, password=request.POST.get('password1'))
                if auth_user:
                    login(request, auth_user)
                return redirect('products:product_list')

    return render(request, 'landing.html', {
        'login_form': login_form,
        'register_form': register_form,
    })