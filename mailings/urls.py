from django.urls import path

from . import views
from .apps import MailingsConfig
from .views import (MailingCreateView, MailingDeleteView, MailingDetailView,
                    MailingListView, MailingRecipientCreateView,
                    MailingRecipientDeleteView, MailingRecipientDetailView,
                    MailingRecipientListView, MailingRecipientUpdateView,
                    MailingUpdateView, recipients_stats_view)
from django.views.decorators.cache import cache_page


app_name = "mailings"

urlpatterns = [
    path("", cache_page(120)(MailingListView.as_view()), name="mailings_list"),
    path("<int:pk>/", cache_page(60)(MailingDetailView.as_view()), name="mailings_detail"),
    path("add/", MailingCreateView.as_view(), name="mailings_add"),
    path("<int:pk>/edit/", MailingUpdateView.as_view(), name="mailings_edit"),
    path("<int:pk>/delete/", MailingDeleteView.as_view(), name="mailings_delete"),
    path("send/<int:pk>/", views.start_mailing, name="start_mailing"),
    path("disable/", views.disable_mailing, name="disable_mailing"),
    # Получатель рассылки
    path("recipients/stats/", recipients_stats_view, name="recipients_stats"),
    path("recipients/", MailingRecipientListView.as_view(), name="recipients_list"),
    path(
        "recipients/<int:pk>/",
        MailingRecipientDetailView.as_view(),
        name="recipient_detail",
    ),
    path("recipients/add/", MailingRecipientCreateView.as_view(), name="recipient_add"),
    path(
        "recipients/<int:pk>/edit/",
        MailingRecipientUpdateView.as_view(),
        name="recipient_edit",
    ),
    path(
        "recipients/<int:pk>/delete/",
        MailingRecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
]
