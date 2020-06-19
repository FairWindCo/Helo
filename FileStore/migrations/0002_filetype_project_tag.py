# Generated by Django 3.0.7 on 2020-06-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileStore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Тип файла',
                'verbose_name_plural': 'Типы файлов',
                'permissions': [('can_add_filetype', 'Может добавлять типы файлов'), ('can_del_filetype', 'Может удалять типы файлов'), ('can_upd_filetype', 'Может изменять типы файлов')],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Тип файла',
                'verbose_name_plural': 'Типы файлов',
                'permissions': [('can_add_project', 'Может добавлять проект'), ('can_del_project', 'Может удалять проект'), ('can_view_project', 'Может просматривать файлы проекта'), ('can_upd_project', 'Может изменять проект')],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Метка',
                'verbose_name_plural': 'Метки',
            },
        ),
    ]
