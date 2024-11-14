from django.contrib import admin
from .models import WaterQualityData

@admin.register(WaterQualityData)
class WaterQualityDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'pH', 'turbidity', 'dissolved_oxygen', 'conductivity', 'temperature', 'nitrate')
    search_fields = ('timestamp',)
    list_filter = ('timestamp', 'pH', 'turbidity', 'temperature')
