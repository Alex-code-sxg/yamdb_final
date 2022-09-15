from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'


class User(AbstractUser):
    USER_ROLES = [
        (ADMIN, ADMIN),
        (USER, USER),
        (MODERATOR, MODERATOR)
    ]
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Недопустимые символы',
            ),
        ]
    )
    email = models.EmailField(
        'Почтовый адрес',
        max_length=254,
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        blank=True,
        max_length=100
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=USER_ROLES,
        default=USER
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
