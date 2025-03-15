from xml.dom.minidom import Comment

from django.contrib import admin

from core.models import Project, ProjectRole, ProjectComment


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['owner','name', 'start_date','end_date','status']
    search_fields = ["name",]
admin.site.register(Project, ProjectAdmin)


class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ['user','project', 'role']
    search_fields = ["project__name"]
admin.site.register(ProjectRole, ProjectRoleAdmin)


class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ['user','text']
    search_fields = ["user__username"]
admin.site.register(ProjectComment, ProjectCommentAdmin)





