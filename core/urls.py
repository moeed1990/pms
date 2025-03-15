from . import views
from django.urls import path

urlpatterns = [
    path("add/", views.create_project, name="create_project"),
    path("view/<int:project_id>/", views.view_project, name="view_project"),
    path("edit/<int:project_id>/", views.edit_project, name="update_project"),
    path("project_list/", views.project_list, name="project_list"),
    path("delete/<int:project_id>/", views.delete_project, name="delete_project"),
]