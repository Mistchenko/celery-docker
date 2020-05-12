from django.contrib import admin
from .models import PriceFile


@admin.register(PriceFile)
class AdminPriceFile(admin.ModelAdmin):
    list_display = ('name', 'file')
    search_fields = ('name',)