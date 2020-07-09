import django_tables2 as tables

from FileStore.models import ProjectFile


class FilesTable(tables.Table):
    created = tables.DateTimeColumn(format='d.m.Y, H:i:s')
    updated = tables.DateTimeColumn(format='d.m.Y, H:i:s')

    class Meta:
        exclude = ('version_before','file_path', 'file_type', 'comments', 'hash')
        model = ProjectFile


class FilesShortTable(tables.Table):
    created = tables.DateTimeColumn(format='d.m.Y, H:i:s')
    updated = tables.DateTimeColumn(format='d.m.Y, H:i:s')

    class Meta:
        exclude = ('version_before', 'file_path', 'file_type', 'comments', 'hash', 'project', 'id')
        model = ProjectFile
