from django.contrib import admin

# Register your models here.
from FileStore.models import Tag, Project, ProjectFile, FileType


class TagAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ['create_user', 'created', 'update_user', 'updated']


admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectFile)
admin.site.register(FileType)
