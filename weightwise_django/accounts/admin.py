from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'user', 'phone_number', 'gender', 'signed_up_at')
    search_fields = ('patient_id', 'user__username', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('gender', 'signed_up_at')
    readonly_fields = ('patient_id', 'signed_up_at')
