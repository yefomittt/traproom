from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import ProjectForm, TaskForm
from .models import Project, Task


def owned_project(request, pk):
    return get_object_or_404(Project.objects.prefetch_related('tasks'), pk=pk, owner=request.user)


@login_required
def projects(request):
    items = Project.objects.filter(owner=request.user).prefetch_related('tasks')
    all_items = list(items)
    stage = request.GET.get('stage', '')
    if stage in Project.Stage.values:
        items = items.filter(stage=stage)
    else:
        stage = ''
    return render(request, 'tracks/projects.html', {
        'projects': items, 'stages': Project.Stage.choices, 'selected_stage': stage,
        'total': len(all_items), 'finished': sum(p.stage == Project.Stage.DONE for p in all_items),
        'remaining': sum(not t.done for p in all_items for t in p.tasks.all()),
    })


@login_required
def project_form(request, pk=None):
    project = owned_project(request, pk) if pk else None
    form = ProjectForm(request.POST if request.method == 'POST' else None, instance=project)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.owner = request.user
        item.save()
        messages.success(request, 'Проект сохранён.')
        return redirect('project', pk=item.pk)
    return render(request, 'tracks/form.html', {'form': form, 'project': project})


@login_required
def project_detail(request, pk):
    project = owned_project(request, pk)
    form = TaskForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()
        return redirect('project', pk=pk)
    return render(request, 'tracks/project.html', {'project': project, 'form': form})


@login_required
def project_delete(request, pk):
    project = owned_project(request, pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект удалён вместе с задачами.')
        return redirect('projects')
    return render(request, 'tracks/delete.html', {'object': project, 'project': project, 'kind': 'проект'})


@login_required
@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    task.done = not task.done
    task.save(update_fields=['done'])
    return redirect('project', pk=task.project_id)


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    form = TaskForm(request.POST if request.method == 'POST' else None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('project', pk=task.project_id)
    return render(request, 'tracks/task_form.html', {'form': form, 'project': task.project})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)
    if request.method == 'POST':
        project_id = task.project_id
        task.delete()
        return redirect('project', pk=project_id)
    return render(request, 'tracks/delete.html', {'object': task, 'project': task.project, 'kind': 'задачу'})
