from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'price', 'created_at')
    search_fields = ('id', 'title', 'author', 'genre', 'price')