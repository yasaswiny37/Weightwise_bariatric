from django.db import migrations

DEFAULT_MODULES = [
    (1, "Introduction to the WeightWise Program", "An overview of the bariatric program, what to expect, and how to use this portal."),
    (2, "Pre-Surgery Nutrition Guidelines", "Dietary guidance and preparation steps before your bariatric procedure."),
    (3, "Understanding Your Procedure", "A walkthrough of the surgical procedure and what happens on the day."),
    (4, "Post-Surgery Recovery", "Recovery timeline, warning signs, and immediate post-op care."),
    (5, "Long-Term Lifestyle & Diet Changes", "Building sustainable eating habits after surgery."),
    (6, "Exercise & Follow-Up Care", "Safe physical activity guidelines and your ongoing follow-up schedule."),
]


def seed_modules(apps, schema_editor):
    Module = apps.get_model('modules', 'Module')
    for order, title, description in DEFAULT_MODULES:
        Module.objects.get_or_create(
            order=order,
            title=title,
            defaults={'description': description, 'is_active': True},
        )


def remove_modules(apps, schema_editor):
    Module = apps.get_model('modules', 'Module')
    titles = [t for _, t, _ in DEFAULT_MODULES]
    Module.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_modules, remove_modules),
    ]
