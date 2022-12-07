# Generated by Django 4.1.3 on 2022-12-06 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_alter_tickets_event_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tickets",
            name="event_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.events"
            ),
        ),
    ]
