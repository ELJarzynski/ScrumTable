# Generated by Django 4.2.11 on 2024-03-09 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='board_id',
            new_name='board',
        ),
    ]
