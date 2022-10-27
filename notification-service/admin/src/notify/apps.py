"""Movie applications."""

from django.apps import AppConfig

from config.settings import DEFAULT_AUTO_FIELD
from django.utils.translation import gettext_lazy as _


class NotifyConfig(AppConfig):
    default_auto_field = DEFAULT_AUTO_FIELD
    name = 'notify'
    verbose_name = _('notify')
