import hashlib
import os

from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from django.urls import reverse


def hash_calculator(file, BUF_SIZE=65536):
    md5 = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.digest()


def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.digest()


class ProjectFile(models.Model):
    filename = models.CharField(max_length=100, verbose_name='Имя файла')
    size = models.PositiveIntegerField(verbose_name='Размер файла')
    hash = models.CharField(max_length=50, verbose_name='ХешКод целостности')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    version_before = models.ForeignKey(to='ProjectFile', on_delete=models.CASCADE, blank=True, null=True, default=None)
    create_user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='created_file',
                                    verbose_name='Кто создал')
    update_user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='modified_file',
                                    verbose_name='Кто изменил')
    project = models.ForeignKey(to='Project', on_delete=models.CASCADE, related_name='project_files',
                                verbose_name='Проект')
    file_path = models.FileField(verbose_name='Путь к файлу', upload_to=MEDIA_ROOT)
    file_type = models.ForeignKey(to='FileType', on_delete=models.CASCADE, blank=True, null=True, default=None)
    comments = models.TextField(max_length=1500, verbose_name='Комментарий', blank=True, null=True)
    tags = models.ManyToManyField(to='Tag', related_name='files', blank=True, verbose_name='Теги')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ('filename', )
        permissions = [('can_add_projectfile', 'Может добавлять файлы проектов'),
                       ('can_del_projectfile', 'Может удалять файлы проектов'),
                       ('can_upd_projectfile', 'Может изменять файлы проектов')]

    def __str__(self):
        return f'{self.filename}({self.size})'

    def get_md5_hash(self, dont_close=False, BUF_SIZE=65536):
        md5 = hashlib.md5()
        try:
            if dont_close:
                f = self.file_path.open('rb')
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    md5.update(data)
            else:
                with self.file_path.open('rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        md5.update(data)
        except FileNotFoundError:
            pass
        return md5.hexdigest()

    def update_hash(self):
        self.hash = self.get_md5_hash(True)

    def check_hash(self):
        return self.hash == self.get_md5_hash()

    def clean(self):
        try:
            self.update_hash()
            self.size = self.file_path.size

            filepath, filename = os.path.split(self.file_path.name)
            if not filepath:
                self.file_path.name = f'{self.project.id}/{self.file_path.name}'

            file, ext = os.path.splitext(self.file_path.path)
            if ext.startswith('.'):
                ext=ext[1:]
            filetype = FileType.objects.get(mask__exact=ext)
            print(file)
            self.file_type = filetype
        except FileType.DoesNotExist:
            pass
        except FileNotFoundError:
            pass

    def get_absolute_url(self):
        return reverse('files-list')


class FileType(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название типа файла')
    mask = models.CharField(max_length=4, verbose_name='Маска для автоопределения', null=True, blank=True)

    class Meta:
        verbose_name = 'Тип файла'
        ordering = ('name',)
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
    tags = models.ManyToManyField(to='Tag', related_name='projects', blank=True, verbose_name='Теги')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ('name',)
        permissions = [('can_add_project', 'Может добавлять проект'),
                       ('can_del_project', 'Может удалять проект'),
                       ('can_view_project', 'Может просматривать файлы проекта'),
                       ('can_upd_project', 'Может изменять проект')]

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('project-update', kwargs={'pk': self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=250, verbose_name='Метка', unique=True)

    def clean(self):
        self.name = self.name.upper()

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name}'
