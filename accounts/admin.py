from django.contrib import admin
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAmin(admin.ModelAdmin):
    list_display=("display_name", "email")
