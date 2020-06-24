import django_tables2 as tables

from FileStore.models import ProjectFile


class FilesTable(tables.Table):
    class Meta:
        exclude = ('version_before','file_path', 'file_type', 'comments')
        model = ProjectFile
