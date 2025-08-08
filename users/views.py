from django.contrib.auth import login
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            return redirect("home")  # перенаправление на главную страницу или dashboard
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def user_statistics(request):
    attempts = SendingAttempt.objects.filter(user=request.user).aggregate(
        total_sent=Count("id"),
        success_count=Count("id", filter=Q(success=True)),
        failure_count=Count("id", filter=Q(success=False)),
    )
    return render(request, "statistics.html", {"stats": attempts})
