# Generated by Django 5.0.3 on 2024-03-28 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_blogpost_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='', max_length=200),
        ),
    ]
