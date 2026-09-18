# Размещение на PythonAnywhere

Подготовка выполнена, публичный сайт пока не развёрнут. Используется бесплатный аккаунт с SQLite и одним веб-приложением. Аккаунт создаёт владелец проекта; условия и срок действия бесплатного сайта нужно проверить в кабинете.

В Bash-консоли PythonAnywhere (выбрать Python 3.12, если он доступен и в настройках Web):

```bash
git clone https://github.com/yefomittt/traproom.git
cd ~/traproom
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python deploy/configure.py YOUR_USERNAME.pythonanywhere.com
export TRAPROOM_CONFIG="$HOME/.config/traproom/production.json"
export DJANGO_SETTINGS_MODULE=studio.production
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py check --deploy
```

Заменить YOUR_USERNAME на логин хостинга. Пароль вводится в консоли, в репозиторий не попадает. Панели администратора в приложении нет; созданный пользователь может войти в обычный интерфейс. Локальные база и пароль не загружаются. Секрет и публичная база хранятся в `~/.config/traproom/` вне исходников. Конфигурацию создают один раз; повторный запуск не перезаписывает секрет.

В разделе Web создать приложение Manual configuration с Python 3.12. Virtualenv: `/home/YOUR_USERNAME/traproom/.venv`. В WSGI-файл из панели Web скопировать содержимое `deploy/pythonanywhere_wsgi.py`. Добавить Static files: URL `/static/`, Directory `/home/YOUR_USERNAME/traproom/staticfiles`. Включить Force HTTPS, нажать Reload.

Проверить по HTTPS вход, CSS, создание трека, задачу, сохранение после перезагрузки страницы и выход. Проверить отсутствие цикла перенаправлений; если он есть, сверить настройки HTTPS с документацией хостинга, не отключать защиту наугад. Сделать резервную копию базы перед последующими изменениями схемы.

Документация: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/

## Code Climate Quality

Требование исходного гайда сохраняется. Code Climate Quality не подключён; бейдж A/B отсутствует. Другой сервис вместо него не выбран. Перенаправление официальной страницы на Qlty не является подтверждением выполнения требования.
