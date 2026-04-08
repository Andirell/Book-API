from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'about', 'role', 'created_at', 'is_staff', 'is_superuser')
    search_fields = ('id', 'email', 'first_name', 'last_name')