from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Mailing, Recipient, SendingAttempt



def index(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="Запущена").count()
    unique_recipients = Recipient.objects.count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_recipients": unique_recipients,
    }
    return render(request, "mailing/index.html", context)


class RecipientListView(ListView):
    model = Recipient
    template_name = "mailing/recipient_list.html"


class RecipientCreateView(CreateView):
    model = Recipient
    template_name = "mailing/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = "mailing/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "mailing/recipient_confirm_delete.html"
    success_url = reverse_lazy("recipient_list")


def run_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if (
        mailing.status != "Запущена"
        and mailing.start_time <= timezone.now() <= mailing.end_time
    ):
        try:
            mailing.send_emails()
            messages.success(request, f'Рассылка "{mailing.id}" успешно запущена.')
        except Exception as e:
            messages.error(request, f"Ошибка при запуске рассылки: {str(e)}")
    else:
        messages.warning(request, "Рассылка уже запущена или время не подходит.")
    return redirect(reverse("index"))


def mailing_attempts(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    attempts = SendingAttempt.objects.filter(mailing=mailing).order_by("-datetime_attempt")
    return render(
        request, "mailings/attempts.html", {"mailing": mailing, "attempts": attempts}
    )
