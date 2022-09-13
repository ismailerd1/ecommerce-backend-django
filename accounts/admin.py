from django.contrib import admin
from .models import Customer


class CustomerFilter(admin.SimpleListFilter):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_filter = ['email']
    ordering = ['first_name', 'last_name']
    

