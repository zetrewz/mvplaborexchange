# Generated by Django 5.0 on 2024-01-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancy', '0002_remove_vacancy_location_alter_vacancy_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='about',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='conditions',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='requirements',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='responsibilities',
            field=models.TextField(),
        ),
    ]
