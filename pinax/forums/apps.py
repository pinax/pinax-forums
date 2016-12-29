from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "pinax.forums"
    label = "pinax_forums"
    verbose_name = "Pinax Fourms"

    def ready(self):
        import_module("pinax.forums.receivers")
