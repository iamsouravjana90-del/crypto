from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import requests

# Register View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('coin_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, 'cryptoapp/register.html', {'form': form})


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('coin_list')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('coin_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'cryptoapp/login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# Coin List View
@login_required
def coin_list_view(request):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': False
    }

    coins = []
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        coins = response.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error fetching coin data: {e}")

    return render(request, 'cryptoapp/coin_list.html', {'coins': coins})
