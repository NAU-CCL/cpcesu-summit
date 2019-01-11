from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'summit.libs.auth'
    label = 'summit_auth'
    verbose_name = "Summit Authentication (Users, Partners, Roles, Permissions)"
