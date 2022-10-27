"""ORM models for Movie application."""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RecipientFilterChoices(models.TextChoices):
    UUID = 'uuid'
    EMAIL = 'email'


class YesNoChoices(models.TextChoices):
    YES = 'yes', _('yes')
    NO = 'no', _('no')


class RepeatChoices(models.TextChoices):
    ANNUALLY = 'annually', _('annually')
    MONTHLY = 'monthly', _('monthly')
    DAILY = 'daily', _('daily')
    HOURLY = 'hourly', _('hourly')


class BodyTemplatesContentTypeChoices(models.TextChoices):
    HTML = 'html', _('html')
    PDF = 'pdf', _('pdf')
    MARKDOWN = 'markdown', _('markdown')


class NotificationTemplatesTypeChoices(models.TextChoices):
    MAIL = 'mail', _('mail')
    SMS = 'sms', _('sms')
    TELEGRAM = 'telegram', _('telegram')
    VIBER = 'viber', _('viber')
    WHATSAPP = 'whatsapp', _('whatsapp')
    PUSH = 'push', _('push')


class NotificationsStatusChoices(models.TextChoices):
    NEW = 'new', _('new')
    SCHEDULED = 'scheduled', _('scheduled')
    COMPLETED = 'completed', _('completed')
    CANCELED = 'canceled', _('canceled')


class TemplatesBody(TimeStampedMixin, UUIDMixin):
    title = models.CharField(_('title'), max_length=255)
    content = models.TextField(_('text_template'))
    content_type = models.CharField(_('content_type'), max_length=255, choices=BodyTemplatesContentTypeChoices.choices)
    description = models.TextField(_('description'), blank=True, null=True)
    conversion_options = models.TextField(_('conversion_options'), blank=True, null=True)  # for PDF

    class Meta:
        db_table = 'notify"."templates_body'
        verbose_name = _('body_template')
        verbose_name_plural = _('body_templates')
        indexes = [
            models.Index(fields=['title'], name='body_templates_title_idx'),
        ]

    def __str__(self):
        return self.title


class Senders(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_('name'), max_length=255, db_index=False)
    email = models.TextField(_('text_template'), db_index=False)

    class Meta:
        db_table = 'notify"."senders'
        verbose_name = _('sender')
        verbose_name_plural = _('senders')


class TemplatesNotify(TimeStampedMixin, UUIDMixin):
    title = models.CharField(_('title'), max_length=255, blank=True, null=True)
    body = models.ForeignKey('TemplatesBody', on_delete=models.CASCADE, db_index=False, blank=True, null=True)
    theme = models.TextField(_('theme'), blank=True, null=True)
    notification_type = models.CharField(_('content_type'), max_length=255, blank=True, null=True,
                                         choices=NotificationTemplatesTypeChoices.choices)
    send_from = models.ForeignKey('Senders', on_delete=models.CASCADE, db_index=False, blank=True, null=True)
    # TODO:  сделать таблицу на которую будет ссылаться recipient_filter с сопоставлениями фильтра и value
    recipient_filter = models.CharField(_('recipient_filter'), max_length=255, blank=True, null=True,
                                        choices=RecipientFilterChoices.choices)
    repeat = models.CharField(_('repeat'), max_length=255, blank=True, null=True, choices=RepeatChoices.choices)
    urgently = models.CharField(_('content_type'), max_length=255, blank=True, null=True, choices=YesNoChoices.choices)
    scheduled_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'notify"."templates_notify'
        verbose_name = _('notification_template')
        verbose_name_plural = _('notification_templates')

    def __str__(self):
        return self.title


class Recipients(TimeStampedMixin, UUIDMixin):
    notification = models.ForeignKey('Notifications', on_delete=models.CASCADE)
    recipient = models.CharField(_('recipient'), max_length=255, blank=True, null=True)
    status_received = models.TextField(_('status_received'), blank=True, null=True)
    is_read = models.CharField(_('is_read'), max_length=255, choices=YesNoChoices.choices)

    class Meta:
        db_table = 'notify"."recipients'
        verbose_name = _('recipient')
        verbose_name_plural = _('recipients')


class Notifications(TimeStampedMixin, UUIDMixin):
    notification_templates = models.ForeignKey('TemplatesNotify', on_delete=models.CASCADE, db_index=False)
    status = models.CharField(_('status_received'), blank=True, null=True, max_length=255,
                              choices=NotificationsStatusChoices.choices)

    class Meta:
        db_table = 'notify"."notifications'
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
