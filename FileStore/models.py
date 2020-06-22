from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ProjectFile(models.Model):
    filename = models.CharField(max_length=100, verbose_name='Имя файла')
    size = models.PositiveIntegerField(verbose_name='Размер файла')
    hash = models.PositiveIntegerField(verbose_name='ХешКод целостности')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    version_before = models.ForeignKey(to='ProjectFile', on_delete=models.CASCADE, blank=True, null=True, default=None)
    create_user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='created_file',
                                    verbose_name='Кто создал')
    update_user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='modified_file',
                                    verbose_name='Кто изменил')
    file_path = models.FileField(verbose_name='Путь к файлу')
    file_type = models.ForeignKey(to='FileType', on_delete=models.CASCADE, blank=True, null=True, default=None)
    comments = models.TextField(max_length=1500, verbose_name='Комментарий', blank=True, null=True)
    tags = models.ManyToManyField(to='Tag', related_name='files', blank=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        permissions = [('can_add_projectfile', 'Может добавлять файлы проектов'),
                       ('can_del_projectfile', 'Может удалять файлы проектов'),
                       ('can_upd_projectfile', 'Может изменять файлы проектов')]

    def __str__(self):
        return f'{self.filename}({self.size})'


class FileType(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название типа файла')
    mask = models.CharField(max_length=4, verbose_name='Маска для автоопределения', null=True, blank=True)

    class Meta:
        verbose_name = 'Тип файла'
        verbose_name_plural = 'Типы файлов'
        permissions = [('can_add_filetype', 'Может добавлять типы файлов'),
                       ('can_del_filetype', 'Может удалять типы файлов'),
                       ('can_upd_filetype', 'Может изменять типы файлов')]

    def __str__(self):
        return f'{self.name}'


class Project(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название проекта')
    comments = models.TextField(max_length=2500, verbose_name='Описание проекта')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    create_user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='created_projects',
                                    verbose_name='Кто создал')
    update_user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='modified_projects',
                                    verbose_name='Кто изменил')
    tags = models.ManyToManyField(to='Tag', related_name='projects', blank=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        permissions = [('can_add_project', 'Может добавлять проект'),
                       ('can_del_project', 'Может удалять проект'),
                       ('can_view_project', 'Может просматривать файлы проекта'),
                       ('can_upd_project', 'Может изменять проект')]

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(max_length=250, verbose_name='Метка', unique=True)

    def clean(self):
        self.name = self.name.upper()

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'

    def __str__(self):
        return f'{self.name}'
