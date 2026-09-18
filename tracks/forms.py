from django import forms
from .models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'bpm', 'musical_key', 'stage', 'notes']
        widgets = {'notes': forms.Textarea(attrs={'rows': 4}),
                   'title': forms.TextInput(attrs={'placeholder': 'Например, Ночной город'}),
                   'musical_key': forms.TextInput(attrs={'placeholder': 'Например, A minor'})}


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title']
        widgets = {'title': forms.TextInput(attrs={'placeholder': 'Что нужно сделать?', 'aria-label': 'Название задачи'})}
