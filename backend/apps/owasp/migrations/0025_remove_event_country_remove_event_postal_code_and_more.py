# Generated by Django 5.1.7 on 2025-03-10 02:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("owasp", "0024_event_country_event_postal_code_event_region"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="country",
        ),
        migrations.RemoveField(
            model_name="event",
            name="postal_code",
        ),
        migrations.RemoveField(
            model_name="event",
            name="region",
        ),
    ]
