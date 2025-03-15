from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.forms import RegisterForm, LoginForm
from core.models import Project, ProjectRole
from core.views import project_list


# Create your views here.
def home(request):
    return redirect('login')
def user_login(request):
    if request.user.is_authenticated:
        return redirect('project_list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('project_list')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('project_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('project_list')
        else:
            messages.error(request, form.errors.as_text())
    else:
        form = RegisterForm()

    return render(request, 'accounts/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required(login_url='login')
def user_manage_role(request):
    project_list_ids = list(Project.objects.filter(owner=request.user).values_list('id', flat=True))
    existing_project_roles = ProjectRole.objects.filter(project_id__in=project_list_ids)
    users = User.objects.filter(projectrole__project__owner=request.user)
    print(users)
    if 'add_user' in request.POST:
        project_user_id = request.POST.get('project_user_id')
        project_role = request.POST.get('project_role')
        project_id = request.POST.get('project_id')
        if project_user_id and project_role and project_id:
            project_roles, created = ProjectRole.objects.get_or_create(user_id=project_user_id, role=project_role, project_id=project_id)
            if not created:
                messages.error(request, "Project role already exists!")
            else:
                messages.success(request, "Project role successfully created!")
        else:
            messages.error(request, "Project role or project role or project role does not exist!")
        return redirect('user_manage_role')



    if 'delete_user' in request.POST:
        delete_project_role_id = request.POST.get('delete_user')
        if delete_project_role_id:
            ProjectRole.objects.get(id=delete_project_role_id).delete()
            messages.success(request, "Project role successfully deleted!")
            return redirect('user_manage_role')

    context = {
        "users":users,
        "existing_users": User.objects.all().exclude(id=request.user.id),
        "existing_projects": Project.objects.filter(owner=request.user),
        "existing_project_roles":existing_project_roles,

    }
    return render(request,'accounts/user_management.html', context)