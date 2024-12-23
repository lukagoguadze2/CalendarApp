import secrets

from celery.result import AsyncResult
from django.db import models
from celery.utils.time import timezone
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from django.utils.text import slugify

from django.conf import settings
from .hasher import generate_user_hash


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    identifier = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)
    university = models.ForeignKey('universities.University', on_delete=models.SET_NULL, null=True, blank=True)
    faculty = models.ForeignKey('universities.Faculty', on_delete=models.SET_NULL, null=True, blank=True)
    year_of_study = models.PositiveIntegerField(null=True, blank=True)

    is_private = models.BooleanField(default=True)
    is_fully_registered = models.BooleanField(default=False)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_profile_slug(self, dict_: bool = False):
        if dict_:
            return {
                'username': slugify(self),
                'hash': generate_user_hash(self.id)
            }

        return f"{slugify(self)}-{generate_user_hash(self.id)}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(
            ('pbkdf2_sha256$', 'bcrypt$', 'argon2')
        ):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Do not change this

    def __repr__(self):
        return f"User({self.id}: {self.email})"


class Group(models.Model):
    group_types = [
        ('L', 'Lecture'),
        ('P', 'Practice'),
        ('S', 'Seminar'),
        ('LB', 'Laboratory'),
    ]

    name = models.CharField(max_length=50)  # Group name (e.g., Group A, Group B)
    course = models.ForeignKey('universities.Course', on_delete=models.CASCADE)
    group_type = models.CharField(max_length=50, choices=group_types)

    def __str__(self):
        return f"{self.name} - {self.course.name}"

    def __repr__(self):
        return f"Group({self.name} - {self.course.name})"


# A user can belong to many groups (many-to-many relationship)
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_group_leader = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        if self.is_group_leader:
            return f"{self.user.username} - Leader of Group {self.group.name}"

        return f"{self.user.username} - {self.group.name}"

    def __repr__(self):
        return f"UserGroup({self.user.username} - {self.group.name})"


class PasswordResetSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    celery_task_id = models.CharField(max_length=255, null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    def is_expired_(self):
        expiration_time = self.created_at + timezone.timedelta(settings.PASSWORD_RESET_SESSION_TIMEOUT)
        return timezone.now() > expiration_time

    def delete(self, *args, **kwargs):
        # NOTE: ეს ლოგიკა არის იმისთვის, რათა მხოლოდ ერთი სესია იყოს აქტიური კონკრეტული იუზერისთვის
        # ამით წინა სესიები დაიხურება ავტომატურად და აქტიური იქნება მხოლოდ ახალი სესია.
        # თუ სესია არის აქტიური, მაშინ გავთიშოთ ის
        if self.celery_task_id:
            task_result = AsyncResult(
                self.celery_task_id
            )  # მოვძებნოთ სელერის ტაკსები და >>

            # შევამოწმოთ ტასკი მუშაობს თუ არა
            if task_result and task_result.status == 'PENDING':
                task_result.revoke()  # თუ მუშაობს მაშინ გავთიშოთ ის
                task_result.forget()

        # ხელით წავშალოთ ყველა არსებული სესია, რომელიც ასოცირებულია იუზერთან
        return super().delete(*args, **kwargs)

    @classmethod
    def generate_token(cls, user):
        token = secrets.token_urlsafe()  # Generate a secure random token
        return cls.objects.create(user=user, token=token)

    def __str__(self):
        return f"Password reset session for {self.user.email}"
