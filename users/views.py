from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractBaseUser
from .models import CustomUser
from .forms import CustomUserCreationForm, LoginForm, CaptchaForm,\
                   SecureLoginForm, PassChForm, CustomUserChangeForm,\
                   ProfileUpdateFrom, LoginChangeForm, EmailChangeForm
from django.contrib.auth.models import User


class UserCreate(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(
            request, 'users/registration.html', context={'form': form}
        )

    def post(self, request):
        if request.method == 'POST':
            bound_form = CustomUserCreationForm(request.POST)
            if bound_form.is_valid():
                new_user = bound_form.save()
                new_user.set_password(bound_form.cleaned_data['password2'])
                new_user.save()
                messages.success(request, 'Аккаунт успешно создан!')
                return redirect('users:login')
        else:
            bound_form = CustomUserCreationForm()
        return render(
               request, 'users/registration.html', context={'form': bound_form}
               )

class UserLogin(View):

    def get(self, request):
        #если попыток входа не было вообще
        if 'try_login' not in request.session:
            #создаем ключ try_login со значением false
            request.session['try_login'] = False
            check_try_login = request.session['try_login']
            #обрабатываем форму без капчи
            form = LoginForm()
        #если попытка входа уже была
        else:
            #запоминаем значение в переменную
            check_try_login = request.session['try_login']
            if not check_try_login:
                # Если попытки входа не было, но сессия try_login есть,
                # то отображаем форму без капчи
                form = LoginForm()
            else:
                # Если попытка входа была, то отображаем форму с капчей
                form = SecureLoginForm()
                captcha_reload = True
        return render(
            request, 'users/login.html', context={'form': form}
        )

    def post(self, request):
        if request.method == 'POST':
            # запоминаем значение try_login в переменную
            check_try_login = request.session['try_login']
            if not check_try_login:
                # Если попытки входа не было, то проверяем и отправляем форму
                # в которой нет поля капчи
                bound_form = LoginForm(request.POST)
                if bound_form.is_valid():
                    cd = bound_form.cleaned_data
                    user = authenticate(
                        request, email=cd['email'], password=cd['password']
                    )
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        messages.success(request, 'Вы успешно вошли в систему!')
                        del request.session['try_login']
                        return redirect('polls:index')
                    else:
                        return HttpResponse('Disabled account')
                else:
                    messages.error(
                        request, 'Неверный ввод данных'
                        )
                    request.session['try_login'] = True
                    return redirect('users:login')
            # Если попытка входа была, то проверяем и отправляем форму
            # в которой есть поле капчи
            else:
                bound_form = SecureLoginForm(request.POST)
                captcha_reload = True
                if bound_form.is_valid():
                    cd = bound_form.cleaned_data
                    user = authenticate(
                        request, email=cd['email'], password=cd['password']
                    )
                else:
                    # если введеная капча не проходит проверку, то
                    # сбрасываем все введенные данные и вызываем ошибку
                    messages.error(
                        request, 'Неверный ввод данных'
                        )
                    return redirect('users:login')
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        messages.success(
                            request,
                            'Вы успешно вошли в систему!'
                        )
                        del request.session['try_login']
                        return redirect('polls:index')
                    else:
                        return HttpResponse('Disabled account')
                else:
                    messages.error(
                        request, 'Неверный ввод данных'
                        )
                    # Если введенные данные пользователя не проходят проверку,
                    # то запоминаем попытку входа, и сбрасываем все введенные
                    # данные
                    request.session['try_login'] = True
                    return redirect('users:login')
        else:
            bound_form = SecureLoginForm()
        return render(
               request, 'users/login.html', context={
                    'form': bound_form,
                    }
               )

def message_change_password(request):
    messages.success(request, 'Вы успешно сменили пароль!')
    return redirect('polls:index')

def logout_view(request):
    logout(request)
    messages.warning(request, 'Вы вышли из системы!')
    return redirect('users:login')
    
class ProfileUser(View):
    def get(self, request):
        p_form = ProfileUpdateFrom(instance=request.user.profile)
        context = {
            'p_form': p_form
        }
        return render(request, 'users/profile.html', context=context)
    def post(self, request):
        p_form = ProfileUpdateFrom(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Изображение обновлено!')
            return redirect('users:account')
        context = {
            'p_form': p_form,
        }
        return render(request, 'users/profile.html', context=context)

class ProfilePassword(View):
    def get(self, request):
        p_form = PassChForm(request.user)
        context = {
            'p_form': p_form
        }
        return render(request, 'users/profile-pas.html', context=context)
    def post(self, request):
        p_form = PassChForm(request.user, request.POST)
        if p_form.is_valid():
            user = p_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменен!')
            return redirect('users:pass_ch')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки!')
        context = {
            'p_form': p_form,
        }
        return render(request, 'users/profile-pas.html', context=context)

class ProfileMail(View):
    def get(self, request):
        p_form = EmailChangeForm(instance=request.user)
        u_form = LoginChangeForm(instance=request.user)
        context = {
            'p_form': p_form,
            'u_form': u_form
        }
        return render(request, 'users/profile-mail.html', context=context)
    def post(self, request):
        p_form = EmailChangeForm(request.POST, instance=request.user)
        u_form = LoginChangeForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, 'Вашы данные успешно обновлены!')
            return redirect('users:login_mail')
        else:
            messages.error(request, 'Такой логин или адрес эл.почты уже зарегистрированы!')
            return redirect('users:login_mail')
        context = {
            'p_form': p_form,
            'u_form': u_form,
        }
        return render(request, 'users/profile-mail.html', context=context)