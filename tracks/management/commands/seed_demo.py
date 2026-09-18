"""Create a local learning account once; never reset an existing password."""
import secrets
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from tracks.models import Project, Task


class Command(BaseCommand):
    help = 'Create a local demo account and example music projects'

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('Demo setup is available only in local DEBUG mode')
        user, created = get_user_model().objects.get_or_create(username='student')
        if not created:
            self.stdout.write('Local account already exists; nothing changed.')
            return
        password = secrets.token_urlsafe(12)
        user.set_password(password)
        user.save()
        examples = [
            ('Ночной город', 140, 'F# minor', 'arrangement', 'Плотный бас, короткий припев. Оставить больше пространства для вокала.', [('Собрать ударные', True), ('Написать бас', True), ('Дописать второй куплет', False), ('Сделать переход', False)]),
            ('Тёплый сигнал', 92, 'A minor', 'mixing', 'Мягкий lo-fi грув. Проверить низ в наушниках и на колонках.', [('Записать клавиши', True), ('Собрать аранжировку', True), ('Почистить низ', False)]),
            ('Первый свет', 124, 'C major', 'idea', 'Светлая мелодия и ровный грув. Начать с восьми тактов.', [('Набросать аккорды', False), ('Подобрать звук синтезатора', False)]),
        ]
        for title, bpm, key, stage, notes, tasks in examples:
            project = Project.objects.create(owner=user, title=title, bpm=bpm, musical_key=key, stage=stage, notes=notes)
            Task.objects.bulk_create([Task(project=project, title=name, done=done) for name, done in tasks])
        path = settings.BASE_DIR / 'local-access.txt'
        path.write_text(f'Только для локальной версии Traproom\nАдрес: http://127.0.0.1:8765/\nЛогин: student\nПароль: {password}\n', encoding='utf-8')
        self.stdout.write(self.style.SUCCESS('Demo created. Credentials saved to ignored local-access.txt'))
