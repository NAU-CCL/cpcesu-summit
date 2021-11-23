from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission

import uuid

from . import choices

from summit.libs.models import AuditModel


def get_all_user_groups():
    user_groups = UserGroup.__subclasses__()
    subclasses = [(1, 'Public')]
    count = 1
    for user_group in user_groups:
        subclasses.append((count, user_group.__name__))
        count += 1
    return subclasses



class UserGroup(AuditModel):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=300, blank=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name='permissions',
        blank=True,
    )
    avatar = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Partner(UserGroup):

    class Meta:
        verbose_name = "Partner"

    def __str__(self):
        return self.name

class CESUnit(UserGroup):

    class Meta:
        verbose_name = "CES Unit"

    def __str__(self):
        return self.name

class CESU(AuditModel):

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=300, blank=True)
    logo = models.ImageField(blank=True)
    # add contact as text field
    contact = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class FederalAgency(UserGroup):

    class Meta:
        verbose_name = "Federal Agency"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """
    Called when the User model needs to be created
    """

    def create_user(self, username, email, password=None):
        """
        Creates a normal user
        :param username: user's username
        :param email: email address
        :param password: the user's password. Default: None
        :return: user model
        """

        if not email:
            raise ValueError("User must have an email address.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        """
        Used to create a super user (CPCESU admin) with all permissions
        :param username: user's username
        :param email: email address
        :param password: password for user. Default: None
        :return: user model
        """

        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        print(user)

        # CPCESU
        group = CESU.objects.get(pk=1)
        print(group)

        # New profile with group
        profile = UserProfile(user=user, first_name=first_name, last_name=last_name, assigned_group=group)
        profile.save(using=self._db)
        print(profile)
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
        return self.username

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
        return self.username + " <" + self.email + ">"

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
    avatar = models.ImageField(blank=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    headshot = models.ImageField(blank=True)

    first_name = models.CharField(default="", max_length=150)
    last_name = models.CharField(default="", max_length=150)

    title = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=150, blank=True)
    address = models.TextField(max_length=300, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    fax_number = models.CharField(max_length=30, blank=True)
    email_address = models.EmailField(blank=True)

    assigned_group = models.ForeignKey(UserGroup, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Assigned Organization")

    def get_full_name(self):
        if self.user is not None:
            return self.first_name + " " + self.last_name
        else:
            return self.first_name + " " + self.last_name

    @staticmethod
    def detail_fields():
        return ['avatar', 'first_name', 'last_name', 'title', 'department', 'location', 'address', 'phone_number',
                'fax_number', 'email_address']

    def __str__(self):
        return self.get_full_name()

    class Meta:
        permissions = (
            ('edit_profile.group', 'Can edit other user profiles of same user group'),
            ('edit_profile.self', 'Can edit own profile'),
            ('view_profile.others', 'Can see other user profiles'),
            ('view_profile.self', 'Can see own profile'),
        )
        verbose_name = "Contact"

class Organization(AuditModel):
    ORG_TYPE = choices.OrganizationChoices.ORG_TYPE

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=300, blank=True)
    logo = models.ImageField(blank=True)
    type = models.CharField(max_length=50, choices=ORG_TYPE,
                            blank=True, verbose_name="Organization Type")
    contact = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.name