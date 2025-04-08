from django.contrib import admin
from .models import Title, Category, Genre, GenreTitle, Review, User
from django.contrib.auth.admin import UserAdmin


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category')
    inlines = [GenreTitleInline, ReviewInline]
    filter_horizontal = ('genre',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'score')
    list_filter = ('score',)
    search_fields = ('text',)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre')

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name',
        'last_name', 'role', 'is_staff'
    )
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 'last_name', 'email', 'bio'
        )}),
        ('Permissions', {'fields': (
            'role', 'is_active', 'is_staff', 'is_superuser'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1',
                'password2', 'role', 'is_staff', 'is_superuser'
            ),
        }),
    )
    filter_horizontal = ()
