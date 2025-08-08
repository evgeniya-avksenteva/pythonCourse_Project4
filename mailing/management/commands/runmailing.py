from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from mailing.models import Mailing


class Command(BaseCommand):
    help = "Запускает рассылку по ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **kwargs):
        mailing_id = kwargs["mailing_id"]
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
            if (
                mailing.status != "Запущена"
                and mailing.start_time <= timezone.now() <= mailing.end_time
            ):
                self.stdout.write(f"Запуск рассылки {mailing_id}...")
                mailing.send_emails()
                self.stdout.write(
                    self.style.SUCCESS(f"Рассылка {mailing_id} успешно выполнена.")
                )
            else:
                self.stderr.write(
                    f"Рассылка {mailing_id} уже запущена или время не подходит."
                )
        except Mailing.DoesNotExist:
            raise CommandError(f"Рассылка с ID {mailing_id} не найдена.")
