# Generated by Django 2.1.3 on 2018-12-08 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MoviesDatabase', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='name',
            new_name='title',
        ),
    ]