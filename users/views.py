from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden
from users.forms import CustomUserRegistrationForm, EditProfileForm
from users.models import EmailConfirmation


def confirm_email(request, token):
    """Функция для обработки ссылки подтверждения"""
    try:
        confirmation = EmailConfirmation.objects.get(token=token)
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()
        return render(request, "users/confirmation_success.html")
    except EmailConfirmation.DoesNotExist:
        return render(request, "users/confirmation_invalid.html")


def register(request):
    """Функция для регистрации, создагния токена и отправки письма"""
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # отключаем до подтверждения email
            user.save()

            # Создаем токен подтверждения
            confirmation = EmailConfirmation.objects.create(user=user)

            # Отправляем письмо с ссылкой на подтверждение
            confirm_url = request.build_absolute_uri(
                reverse("users:confirm_email", args=[str(confirmation.token)])
            )
            send_mail(
                "Подтверждение регистрации",
                f"Перейдите по ссылке для подтверждения: {confirm_url}",
                "your_email@example.com",
                [user.email],
            )

            return render(
                request, "users/registration_pending.html"
            )  # страница с инструкциями
    else:
        form = CustomUserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def registration_pending(request):
    return render(request, "users/registration_pending.html")


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("users:home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("users:login")


def user_profile(request):
    return render(request, "users/profile.html")

@login_required
def edit_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Вы должны войти в систему.")
    # остальной код
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


def home(request):
    return render(request, "users/home.html")
