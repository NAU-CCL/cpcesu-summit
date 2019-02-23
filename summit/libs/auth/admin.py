from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from summit.libs.auth.models import User, UserProfile, Partner, CESUnit, FederalAgency


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users with a password confirmation field.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active')

    def clean_password(self):
        """
        Checks that both of the passwords match
        :return: String - Password or Boolean False otherwise
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        """
        Save data, mostly the password, in a hashed form
        :param commit: Whether or not to commit the change to DB
        :return: user model with hashed password
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class UserChangeForm(forms.ModelForm):
    """
    For updating users. Includes all fields but replaces the password field with the hash display field
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        """
        Sets the initial password
        :return: initialized password
        """
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    """
    For adding and changing users
    """

    form = UserChangeForm
    add_form = UserCreationForm

    # For displaying the user model
    list_display = ('username', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    readonly_fields = ('date_joined', 'last_login', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'user_permissions', 'group')}),
        ('Auditing', {'fields': ('is_active', 'date_joined', 'last_login')}),
    )

    # Adding new user fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_admin')
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    ordering = ('username', 'email', 'first_name', 'last_name', 'is_admin')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Partner)
admin.site.register(CESUnit)
admin.site.register(FederalAgency)
admin.site.register(UserProfile)
admin.site.register(Permission)
admin.site.unregister(Group)
