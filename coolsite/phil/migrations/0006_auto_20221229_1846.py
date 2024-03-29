# Generated by Django 3.2.7 on 2022-12-29 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phil', '0005_auto_20221129_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Статья'),
        ),
        migrations.AddField(
            model_name='articles',
            name='text_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Статья'),
        ),
        migrations.AddField(
            model_name='articles',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='articles',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='books',
            name='author_description_en',
            field=models.TextField(null=True, verbose_name='Описание автора / издательства'),
        ),
        migrations.AddField(
            model_name='books',
            name='author_description_ru',
            field=models.TextField(null=True, verbose_name='Описание автора / издательства'),
        ),
        migrations.AddField(
            model_name='books',
            name='author_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Автор(ы)'),
        ),
        migrations.AddField(
            model_name='books',
            name='author_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Автор(ы)'),
        ),
        migrations.AddField(
            model_name='books',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='books',
            name='name_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Название'),
        ),
    ]
