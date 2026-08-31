from django.contrib import admin
from .models import Module, ModuleProgress


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'is_active', 'slide_deck', 'video')
    list_editable = ('is_active',)
    ordering = ('order',)


@admin.register(ModuleProgress)
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ('patient', 'module', 'viewed', 'completed', 'completed_at')
    list_filter = ('completed', 'viewed', 'module')
    search_fields = ('patient__patient_id', 'patient__user__username')
