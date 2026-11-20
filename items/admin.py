
from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'item_type',
        'category',
        'reported_by',
        'created_at',
    )

    list_filter = ('item_type', 'category')
    search_fields = ('name', 'location')

    readonly_fields = ('created_at',)
