# Traproom

[![Maintainability](https://qlty.sh/gh/yefomittt/projects/traproom/maintainability.svg)](https://qlty.sh/gh/yefomittt/projects/traproom)

Учебное веб-приложение для музыкальных проектов: карточки треков с темпом, тональностью и этапом работы, заметки, задачи и прогресс. Каждый пользователь видит только свои данные. Сайт: https://yefomittt.pythonanywhere.com/.

## Учебная основа и вклад

Выбранный пункт каталога: **Build a Todo List with Django and Test-Driven Development**.

- Каталог: https://github.com/practical-tutorials/project-based-learning#python
- Учебник: https://www.obeythetestinggoat.com/

Проект использует идею списка задач на Django. Код учебника не копировался, полное прохождение книги не заявляется. Предметные дополнения: музыкальный проект, BPM, тональность, этап производства, заметки, фильтр этапов и вычисление прогресса. Музыкальную адаптацию ещё следует подтвердить у руководителя практики. История коммитов отражает реальные этапы создания проекта.

## Технологии

- Интерфейс: HTML, Django Templates, CSS; без отдельной сборки JavaScript.
- Сервер: Python 3.12, Django 5.2.
- Данные: SQLite. База сохраняется в локальном `db.sqlite3`.
- Тесты: Django TestCase, тестовая база изолирована от пользовательской.

## Быстрый запуск на этом компьютере

Дважды нажмите `start-local.cmd`. Оставьте открывшееся окно работающим. Откройте http://127.0.0.1:8765/. Локальные данные входа находятся в `local-access.txt`. Для остановки нажмите Ctrl+C в окне сервера. Никакие файлы автоматически в интернет не отправляются.

## Установка на другом компьютере

Нужны Python 3.12+ и браузер. В PowerShell из папки проекта:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8765
```

Команда `seed_demo` создаёт пользователя `student` и три демонстрационных трека. Пароль генерируется случайно и записывается только в игнорируемый Git файл `local-access.txt`. Повторный вызов не сбрасывает пароль и не дублирует проекты. Публичной регистрации в первой версии нет; дополнительного пользователя разработчик может создать средствами Django.

## Проверка

```powershell
python manage.py check
python manage.py test
```

Проверяются вход, создание и изменение проектов, границы BPM, задачи и прогресс, фильтр, удаление, изоляция пользователей, CSRF и экранирование пользовательского текста.

## Структура

`tracks/models.py` — таблицы; `forms.py` — формы и проверка ввода; `views.py` — действия; `urls.py` — адреса; `templates/` — страницы; `static/style.css` — оформление. HTML-формы отправляют запросы непосредственно Django; отдельного JSON API в этой версии нет.

## Публикация и проверка качества

- Сайт: https://yefomittt.pythonanywhere.com/
- Репозиторий: https://github.com/yefomittt/traproom
- Результат Qlty: https://qlty.sh/gh/yefomittt/projects/traproom
- Инструкция для размещения: [docs/deployment.md](docs/deployment.md).

Qlty используется как новая версия Code Climate Quality. Бейдж показывает текущую оценку поддерживаемости кода; результаты безопасности доступны отдельно на странице анализа. Приемлемость Qlty для требования учебного гайда нужно подтвердить у руководителя практики. Запись демонстрации и окончательный отчёт ещё готовятся.
