# from django.core.management.base import BaseCommand
#
# from mailings.models import Mailing
#
#
# class Command(BaseCommand):
#     help = "Отправка активных рассылок"
#
#     def handle(self, *args, **kwargs):
#         mailings_to_send = Mailing.objects.filter(status="Запущена")
#         for mailings in mailings_to_send:
#             self.stdout.write(f"Обработка рассылки ID={mailings.id}")
#             mailings.send_emails()
#             # Обновляем статус после завершения
#             mailings.status = "Завершена"
#             mailings.save()
