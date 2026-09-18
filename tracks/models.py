from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Project(models.Model):
    class Stage(models.TextChoices):
        IDEA = 'idea', 'Идея'
        ARRANGEMENT = 'arrangement', 'Аранжировка'
        MIXING = 'mixing', 'Сведение'
        MASTERING = 'mastering', 'Мастеринг'
        DONE = 'done', 'Готово'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField('Название трека', max_length=120)
    bpm = models.PositiveSmallIntegerField('Темп (BPM)', default=120, validators=[MinValueValidator(20), MaxValueValidator(300)])
    musical_key = models.CharField('Тональность', max_length=30, blank=True)
    stage = models.CharField('Этап', max_length=20, choices=Stage.choices, default=Stage.IDEA)
    notes = models.TextField('Заметки', blank=True, max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return self.title

    @property
    def progress(self):
        tasks = list(self.tasks.all())
        return round(sum(task.done for task in tasks) * 100 / len(tasks)) if tasks else 0


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField('Задача', max_length=200)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'pk']

    def __str__(self):
        return self.title
