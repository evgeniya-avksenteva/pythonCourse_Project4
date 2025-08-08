from django.urls import path
from .views import index, RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView
from . import views

urlpatterns = [
    path("", index, name="index"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/add/", RecipientCreateView.as_view(), name="recipient_add"),
    path("recipients/<int:pk>/edit/", RecipientUpdateView.as_view(), name="recipient_edit"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path('mailing/<int:pk>/send/', views.run_mailing, name='run_mailing'),
]
