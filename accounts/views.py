from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from books.models import UserBalance, EbookPurchase, Order

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    next_url = request.POST.get('next') or request.GET.get('next') or 'home'
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')

@login_required
def profile(request):
    balance, _ = UserBalance.objects.get_or_create(user=request.user)
    purchases = EbookPurchase.objects.filter(user=request.user).select_related('book', 'book__author')
    orders = Order.objects.filter(user=request.user).prefetch_related('items__book')
    return render(request, 'accounts/profile.html', {
        'balance': balance,
        'purchases': purchases,
        'orders': orders,
    })
