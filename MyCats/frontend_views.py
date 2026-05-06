from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from cats.models import Cat
from frontend_forms import LoginForm, RegisterForm, CatForm, EditProfileForm

User = get_user_model()


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли')
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Учетная запись создана успешно!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
def my_cats(request):
    cats = Cat.objects.filter(owner=request.user)
    return render(request, 'my_cats.html', {'cats': cats})


@login_required(login_url='login')
def add_cat(request):
    if request.method == 'POST':
        form = CatForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.owner = request.user
            cat.save()
            messages.success(request, f'Кошка {cat.name} добавлена!')
            return redirect('my-cats')
    else:
        form = CatForm()
    return render(request, 'add_cat.html', {'form': form})


@login_required(login_url='login')
def edit_cat(request, pk):
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CatForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, f'Кошка {cat.name} обновлена!')
            return redirect('my-cats')
    else:
        form = CatForm(instance=cat)
    return render(request, 'add_cat.html', {'form': form, 'cat': cat})


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def delete_cat(request, pk):
    cat = get_object_or_404(Cat, pk=pk, owner=request.user)
    if request.method == 'POST':
        cat_name = cat.name
        cat.delete()
        messages.success(request, f'Кошка {cat_name} удалена!')
        return redirect('my-cats')
    return render(request, 'confirm_delete.html', {'cat': cat})


@login_required(login_url='login')
def profile(request):
    cats_count = Cat.objects.filter(owner=request.user).count()
    return render(request, 'profile.html', {'cats_count': cats_count})


@login_required(login_url='login')
def chat(request):
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'chat.html', {'users': users})


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        from django.contrib.auth.forms import PasswordChangeForm
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            login(request, form.user)
            messages.success(request, 'Пароль изменен!')
            return redirect('profile')
    else:
        from django.contrib.auth.forms import PasswordChangeForm
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
