from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

import uuid

from summit.libs.models import AuditModel


class UserManager(BaseUserManager):
    """
    Called when the User model needs to be created
    """
    def create_user(self, username, email, first_name, last_name, password=None):
        """
        Creates a normal user
        :param username: user's username
        :param email: email address
        :param first_name: first name
        :param last_name: last name
        :param password: the user's password. Default: None
        :return: user model
        """

        if not email:
            raise ValueError("User must have an email address.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        """
        Used to create a super user (CPCESU admin) with all permissions
        :param username: user's username
        :param email: email address
        :param first_name: first name
        :param last_name: last name
        :param password: password for user. Default: None
        :return: user model
        """

        user = self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    User model
    """
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False,
                                   help_text="With this checked, it allows this user to access the administrative " +
                                             "backend",
                                   verbose_name="Admin site access?")

    first_name = models.CharField(blank=False, max_length=150)
    last_name = models.CharField(blank=False, max_length=150)

    external_id = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        default=uuid.uuid4
    )

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        """
        Returns the first and last names of the user
        :return: first and last names as a concat string
        """
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        """
        Returns the user's email
        :return: user's email address as string
        """
        return self.username

    def __str__(self):
        """
        User's email
        :return: user's email address
        """
        return self.first_name + " " + self.last_name + " <" + self.email + ">"

    def has_perm(self, perm, obj=None):
        """
        #TODO: Add actual functionality
        :param perm:
        :param obj:
        :return:
        """
        return True

    def has_module_perms(self, app_label):
        """
        #TODO: Add actual functionality
        :param app_label:
        :return:
        """
        return True

    @property
    def is_staff(self):
        """
        Returns if administrator (all perms
        :return: Boolean, true or false on self.is_admin
        """
        return self.is_admin

    @property
    def is_superstaff(self):
        return self.is_superuser


class UserProfile(AuditModel):
    user = models.OneToOneField(User)
    avatar = models.ImageField()

    class Meta:
        verbose_name = "User Profile"


class Partner(AuditModel):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=300, blank=True)


