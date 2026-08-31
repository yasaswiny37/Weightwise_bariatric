from django.db import models


class Module(models.Model):
    """
    One learning module in the bariatric program.
    Right now content is a PPT slide deck; a video field is already here
    so it can be filled in later without changing the database structure.
    """
    order = models.PositiveIntegerField(default=0, help_text="Controls the display order (1-6, etc.)")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slide_deck = models.FileField(
        upload_to='module_slides/',
        blank=True,
        null=True,
        help_text="Upload the .ppt/.pptx file for this module"
    )
    video = models.FileField(
        upload_to='module_videos/',
        blank=True,
        null=True,
        help_text="Leave empty for now — reserved for when video content is added"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order}. {self.title}"


class ModuleProgress(models.Model):
    """Tracks whether a patient has viewed/completed a given module."""
    patient = models.ForeignKey('accounts.Patient', on_delete=models.CASCADE, related_name='progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='progress_records')
    viewed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    first_viewed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('patient', 'module')

    def __str__(self):
        return f"{self.patient} - {self.module} ({'done' if self.completed else 'in progress'})"
