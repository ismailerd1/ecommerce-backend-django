from django.contrib import admin

from accounts.models import Customer


class CustomerFilter(admin.SimpleListFilter):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']
    list_filter = ['user__email']
    ordering = ['user__first_name', 'user__last_name', 'phone']
    autocomplete_fields = ['user']
