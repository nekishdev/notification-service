from typing import Optional

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.db.models.query import QuerySet

from movies.models import Filmwork, PersonFilmwork


def _prepare_role_array_agg(role: str) -> ArrayAgg:
    """
    Подготовить агрегацию участников конкретной роли.
    """
    return ArrayAgg('persons__full_name', filter=Q(personfilmwork__role=role), distinct=True)


def _prepare_genres_array_agg() -> ArrayAgg:
    """
    Подготовить агрегацию жанров.
    """
    return ArrayAgg('genres__name', filter=Q(genres__name__isnull=False), distinct=True)


class MoviesApiMixin:
    model = Filmwork

    def get_queryset(self):
        return self.model.objects\
            .values('id',
                    'title',
                    'description',
                    'creation_date',
                    'rating',
                    'type')\
            .annotate(genres=_prepare_genres_array_agg())\
            .annotate(actors=_prepare_role_array_agg(PersonFilmwork.Role.actor))\
            .annotate(directors=_prepare_role_array_agg(PersonFilmwork.Role.director))\
            .annotate(writers=_prepare_role_array_agg(PersonFilmwork.Role.writer))\
            .all()

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    http_method_names = ['get']
    paginate_by = 50

    def _paginate(self) -> QuerySet:
        self.paginator, self.page, queryset, _ = self.paginate_queryset(
            self.get_queryset(),
            self.paginate_by
        )
        return queryset

    def _get_next_page_number(self) -> Optional[int]:
        return self.page.next_page_number() if self.page.has_next() else None

    def _get_previous_page_number(self) -> Optional[int]:
        return self.page.previous_page_number() if self.page.has_previous() else None

    def _get_total_pages(self) -> int:
        return self.paginator.num_pages

    def _get_total_count(self) -> int:
        return self.paginator.count

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self._paginate()

        return {
            'count': self._get_total_count(),
            'total_pages': self._get_total_pages(),
            'prev': self._get_previous_page_number(),
            'next': self._get_next_page_number(),
            'results': list(queryset)
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    model = Filmwork
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        return self.object
