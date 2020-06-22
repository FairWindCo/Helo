from django.contrib import admin

# Register your models here.
from FileStore.models import Tag, Project, ProjectFile, FileType


class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
admin.site.register(Project)
admin.site.register(ProjectFile)
admin.site.register(FileType)