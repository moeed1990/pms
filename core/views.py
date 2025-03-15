from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from core.forms import ProjectForm
from core.models import Project, ProjectRole, ProjectComment
from core.project_permissions import has_project_permission


# Create your views here.
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Project successfully created')
            return redirect('project_list')
        else:
            print(form.errors)
            messages.error(request, form.errors.as_text())

    return render(request, 'projects/edit_project.html', {'form': form})

@login_required(login_url='login')
@has_project_permission(required_roles=['owner', 'editor'])
def edit_project(request, project_id):
    project_obj = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(instance=project_obj)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project_obj)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project successfully updated')
            return redirect('project_list')
        else:
            print(form.errors)
            messages.error(request, form.errors.as_text())

    return render(request, 'projects/edit_project.html', {'form': form})


@login_required(login_url='login')
@has_project_permission(required_roles=['owner', 'editor', 'reader'])
def view_project(request, project_id):
    project_obj = get_object_or_404(Project, pk=project_id)
    project_comments = ProjectComment.objects.filter(project=project_obj)
    if 'add_comments' in request.POST:
        comment = request.POST.get('comment')
        if comment:
            if 'reader' in project_obj.permission_list(request.user):
                return HttpResponseForbidden("You don't have permission to comment on this project.")
            ProjectComment.objects.create(user=request.user, project=project_obj, text=comment)
    return render(request, 'projects/view_project.html', {'project_obj': project_obj, "project_comments":project_comments})

def project_list(request):
    assign_role_user_charity = list(ProjectRole.objects.filter(user=request.user).values_list('project_id', flat=True))
    projects = Project.objects.filter(Q(owner=request.user)| Q(id__in=assign_role_user_charity))

    context = {
        "projects": projects
    }
    return render(request,'projects/project_list.html', context)

@login_required(login_url='login')
@has_project_permission(required_roles=['owner'])
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return redirect('project_list')


