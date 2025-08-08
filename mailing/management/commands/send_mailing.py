from django.core.management.base import BaseCommand
from mailing.models import Mailing


class Command(BaseCommand):
    help = "Отправка активных рассылок"

    def handle(self, *args, **kwargs):
        mailings_to_send = Mailing.objects.filter(status="Запущена")
        for mailing in mailings_to_send:
            self.stdout.write(f"Обработка рассылки ID={mailing.id}")
            mailing.send_emails()
            # Обновляем статус после завершения
            mailing.status = "Завершена"
            mailing.save()
