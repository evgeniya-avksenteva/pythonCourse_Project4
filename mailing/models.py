from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from config import settings


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Создана")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    name = models.CharField(max_length=255, null=True, blank=True)
    # добавляем поле владельца
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
        default=1,
    )

    def __str__(self):
        return self.name

    def set_status(self, new_status):
        self.status = new_status
        self.save()

    def send_emails(self):
        # Обновляем статус перед отправкой
        self.set_status("Запущена")
        success_count = 0
        failure_count = 0
        for recipient in self.recipients.all():
            try:
                # Отправка письма
                send_mail(
                    subject=self.message.subject,
                    message=self.message.body,
                    from_email="evgeniya.avk@yandex.ru",
                    recipient_list=[recipient.email],
                )
                # Логируем успешную попытку
                SendAttempt.objects.create(
                    mailing=self,
                    recipient=recipient.email,
                    attempt_time=timezone.now(),
                    server_response="Письмо успешно отправлено",
                    status="Успешно",
                )
                success_count += 1
            except Exception as e:
                # Логируем ошибку
                SendAttempt.objects.create(
                    mailing=self,
                    recipient=recipient.email,
                    attempt_time=timezone.now(),
                    server_response=str(e),
                    status="Не успешно",
                )
                failure_count += 1
        # Обновляем статус после завершения
        self.set_status("Завершена")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class SendAttempt(models.Model):
    STATUS_CHOICES = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]

    attempt_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, null=True, blank=True)
    server_response = models.CharField(max_length=255, null=True, blank=True)
    mailing = models.ForeignKey(
        "Mailing", on_delete=models.CASCADE, null=True, blank=True
    )
    recipient = models.EmailField(max_length=254)

    class Meta:
        verbose_name = "Попытка отправки"
        verbose_name_plural = "Попытки отправки"
