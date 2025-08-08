from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "avatar", "phone_number", "country"]
