from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from ...models import TemplatesBody, TemplatesNotify, Notifications


class TemplatesBodyApiMixin:
    http_method_names = ['get']

    @staticmethod
    def render_to_response(context, **response_kwargs):
        return JsonResponse(context)

    @classmethod
    def get_queryset(cls):
        fields = ('id', 'title', 'text_template', 'content_type', 'description', 'conversion_options')
        return TemplatesBody.objects.values(*fields)


class TemplatesBodyListApi(TemplatesBodyApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class TemplatesBodyDetailApi(TemplatesBodyApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)['object']


class TemplatesNotifyApiMixin:
    http_method_names = ['get']

    @staticmethod
    def render_to_response(context, **response_kwargs):
        return JsonResponse(context)

    @classmethod
    def get_queryset(cls):
        fields = ('id', 'title', 'body_id', 'theme', 'notification_type',
                  'send_from_id', 'recipient_filter', 'repeat',
                  'urgently', 'scheduled_time')
        return TemplatesNotify.objects.values(*fields)


class TemplatesNotifyListApi(TemplatesNotifyApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class TemplatesNotifyDetailApi(TemplatesNotifyApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)['object']


class NotificationsApiMixin:
    http_method_names = ['get']

    @staticmethod
    def render_to_response(context, **response_kwargs):
        return JsonResponse(context)

    @classmethod
    def get_queryset(cls):
        fields = ('id', 'notification_templates_id', 'status')
        return Notifications.objects.values(*fields)


class NotificationsListApi(NotificationsApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class NotificationsDetailApi(NotificationsApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)['object']
