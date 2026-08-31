from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    """
    Extends the built-in Django User with hospital-patient specific fields.
    Created automatically the moment someone signs up on the site.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other / Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    patient_id = models.CharField(max_length=20, unique=True, blank=True)
    signed_up_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Simple sequential-looking hospital patient ID, e.g. WW-000001
            last = Patient.objects.order_by('id').last()
            next_num = (last.id + 1) if last else 1
            self.patient_id = f"WW-{next_num:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.patient_id})"
