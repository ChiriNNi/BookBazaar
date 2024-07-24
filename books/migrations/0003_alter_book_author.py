# Generated by Django 5.0.6 on 2024-07-22 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_author_alter_book_options_book_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.author', verbose_name='Автор'),
        ),
    ]
