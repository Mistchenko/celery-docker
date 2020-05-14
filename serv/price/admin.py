from django.contrib import admin
from .models import PriceFile, PriceList


@admin.register(PriceFile)
class AdminPriceFile(admin.ModelAdmin):
    list_display = ('name', 'params', 'file', 'status', 'log', 'date_updated', 'date_create',)
    search_fields = ('name',)


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ('part_num', 'name', 'price', 'price_name', 'date_updated',)
    search_fields = ('part_num', 'name', 'price_name',)