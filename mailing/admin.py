from django.contrib import admin
from .models import Recipient, Message, Mailing


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "comment")
    search_fields = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "start_time", "end_time")
    list_filter = ("status",)
    search_fields = ("id",)

# @admin.register(MailingAttempt)
# class MailingAttemptAdmin(admin.ModelAdmin):
#     list_display = ("id", "attempt_time", "status", "mailing")
#     list_filter = ("status", "mailing")


search_fields = ("mailing__id",)
