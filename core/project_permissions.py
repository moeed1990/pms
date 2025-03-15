from django.http import HttpResponseForbidden
from .models import ProjectRole, Project


def has_project_permission(required_roles):
    def decorator(view_func):
        def _wrapped_view(request, project_id, *args, **kwargs):
            project = Project.objects.get(id=project_id)

            if project.owner == request.user:
                return view_func(request, project_id, *args, **kwargs)

            project_roles = ProjectRole.objects.filter(user=request.user, project=project).first()
            if not project_roles or project_roles.role not in required_roles:
                return HttpResponseForbidden("You don't have permission to access this project.")

            return view_func(request, project_id, *args, **kwargs)

        return _wrapped_view
    return decorator
