from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name',
        'year', 'description',
        'get_genre', 'category'
    )
    search_fields = ('name', 'description')
    list_filter = ('name', 'year',)
    empty_value_display = '-пусто-'

    def get_genre(self, obj):
        return "\n".join([p.genre for p in obj.genre.all()])


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
