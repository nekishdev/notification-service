from django.contrib import admin

from .models import Genre, GenreFilmwork, Person, PersonFilmwork, Filmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork

    autocomplete_fields = ('person',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = [GenreFilmworkInline, PersonFilmworkInline]

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)

    # Фильтрация в списке
    list_filter = ('type',)

    search_fields = ('title', 'description', 'id',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('genres', 'persons')
