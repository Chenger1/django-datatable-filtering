# Generated by Django 4.0.2 on 2022-02-18 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('customer', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('text', models.TextField()),
                ('another_text', models.CharField(max_length=255)),
                ('boolean_field', models.BooleanField(default=False)),
            ],
        ),
    ]
