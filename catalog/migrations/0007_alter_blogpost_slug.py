# Generated by Django 5.0.3 on 2024-03-25 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_blogpost_views_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]