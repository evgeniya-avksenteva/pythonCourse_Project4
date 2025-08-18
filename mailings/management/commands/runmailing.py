# from django.core.management.base import BaseCommand, CommandError
# from django.utils import timezone
#
# from mailings.models import Mailing
#
#
# class Command(BaseCommand):
#     help = "Запускает рассылку по ID"
#
#     def add_arguments(self, parser):
#         parser.add_argument("mailing_id", type=int)
#
#     def handle(self, *args, **kwargs):
#         mailing_id = kwargs["mailing_id"]
#         try:
#             mailings = Mailing.objects.get(pk=mailing_id)
#             if (
#                 mailings.status != "Запущена"
#                 and mailings.start_time <= timezone.now() <= mailings.end_time
#             ):
#                 self.stdout.write(f"Запуск рассылки {mailing_id}...")
#                 mailings.send_emails()
#                 self.stdout.write(
#                     self.style.SUCCESS(f"Рассылка {mailing_id} успешно выполнена.")
#                 )
#             else:
#                 self.stderr.write(
#                     f"Рассылка {mailing_id} уже запущена или время не подходит."
#                 )
#         except Mailing.DoesNotExist:
#             raise CommandError(f"Рассылка с ID {mailing_id} не найдена.")
