# Generated by Django 3.0 on 2019-12-14 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drugs', '0007_pharmacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pharmacy',
            name='pharmacist',
            field=models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
