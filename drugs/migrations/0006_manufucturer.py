# Generated by Django 3.0 on 2019-12-12 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drugs', '0005_auto_20191211_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufucturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('registration_number', models.CharField(blank=True, max_length=100, unique=True)),
                ('country', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufucturer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
