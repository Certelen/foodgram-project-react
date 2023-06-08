# FOODGRAM
## Продуктовый помощник
Сервис позволяет регистрироваться, создавать и публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин - скачивать  список продуктов, нужных для приготовления рецептов.
## Технологии
[![Foodgram workflow](https://github.com/Certelen/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/Certelen/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)
## Установка
Клонируем репозиторий и переходим в директорию infra:
```
git clone https://github.com/Certelen/foodgram-project-react.git
cd ./foodgram-project-react/infra/
```
Требуется изменить ALLOWED_HOSTS в ./backend/frontend/frontend/settings.py и server_name в ./infra/nginx/default.conf
## Подготовка сервера:
1. Перейдите на боевой сервер:
```
ssh username@server_address
```
2. Обновите индекс пакетов APT:
```
sudo apt update
```
и обновите установленные в системе пакеты и установите обновления безопасности:
```
sudo apt upgrade -y
```
Создайте папку `nginx` и `docs`:
```
mkdir nginx
mkdir docs
``` 
Скопируйте файлы docker-compose.yaml, nginx/default.conf, ../docs/redoc.html, ../docs/openapi-schema.yml из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml, home/<ваш_username>/nginx/default.conf, home/<ваш_username>/docs/redoc.html, home/<ваш_username>/docs/openapi-schema.yml соответственно:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
scp redoc.html <username>@<host>/home/<username>/docs/redoc.html
scp openapi-schema.yml <username>@<host>/home/<username>/docs/openapi-schema.yml
```
Установите Docker и Docker-compose:
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте правильность установки Docker-compose:
```
sudo  docker-compose --version
```
На боевом сервере создайте файл .env:
```
touch .env
```
и заполните переменные окружения
```
nano .env
SECRET_KEY=<SECRET_KEY>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=xxxyyyzzz
DB_HOST=db
DB_PORT=5432
```
## Workflow:
1. tests - Проверка проекта на соответствие стандартам PEP8.
2. build - Сборка и доставка докер-образов на Docker Hub
3. deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер.
4. send_message - Отправка уведомления в Telegram

В репозитории на Github.com добавьте данные в **`Settings - Secrets - Actions secrets`**:
* ```DOCKER_USERNAME``` - имя пользователя в DockerHub (Только строчные буквы)
* ```DOCKER_PASSWORD``` - пароль пользователя в DockerHub
* ```HOST``` - адрес боевого сервера
* ```USER``` - пользователь
* ```SSH_KEY``` - приватный ssh-ключ с компьютера, имеющего доступ к боевому серверу
* ```PASSPHRASE``` - кодовая фраза для ssh-ключа (Если было указано при создании ssh-ключа)
* ```DB_ENGINE``` - django.db.backends.postgresql
* ```DB_NAME``` - postgres (по умолчанию)
* ```POSTGRES_USER``` - postgres (по умолчанию)
* ```POSTGRES_PASSWORD``` - xxxyyyzzz (по умолчанию)
* ```DB_HOST``` - db
* ```DB_PORT``` - 5432
* ```SECRET_KEY``` - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
* ```TELEGRAM_TO``` - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
* ```TELEGRAM_TOKEN``` - токен бота (получить токен можно у @BotFather, /token, имя бота)
При внесении изменений в проект:
```
git add .
git commit -m "..."
git push
```
запускается набор блоков команд (см. файл [foodgram_workflow.yml](https://github.com/Certelen/foodgram-project-react/blob/master/.github/workflows/foodgram_workflow.yml), т.к. команда `git push` является триггером workflow проекта.  

## Развертывание проекта с помощью Docker:
Разворачиваем контейнеры в фоновом режиме из папки infra:
```
sudo docker compose up -d
```
При первом запуске выполняем миграции:
```
sudo docker compose exec backend python manage.py migrate
```
При первом запуске собираем статику:
```
sudo docker compose exec backend python manage.py collectstatic --no-input
```
Создайте суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```
Загружаем данные ингредиентов в базу данных:
```
sudo docker compose exec backend python manage.py loaddata dump.json
```
## Пользовательские роли в проекте
1. Анонимный пользователь
2. Аутентифицированный пользователь
3. Администратор

### Что могут анонимные пользователи могут:
1. Просматривать список рецептов;
2. Просматривать отдельные рецепты;
3. Просматривать страницы пользователей;
4. Фильтровать рецепты по тегам;
5. Создавать аккаунт.

### Что могут аутентифицированные пользователи могут:
1. Входить в систему под своим логином и паролем;
2. Выходить из системы (разлогиниваться);
3. Получать данные о своей учетной записи;
4. Изменять свой пароль;
5. Просматривать, публиковать, удалять и редактировать свои рецепты;
6. Добавлять понравившиеся рецепты в избранное и удалять из избранного;
7. Добавлять рецепты в список покупок и удалять из списка;
8. Подписываться и отписываться на авторов;
9. Скачивать список покупок.

### Эндпоинты:
- ```api/docs/redoc.html``` - Подробная документация по работе API.
- ```api/tags/``` - Получение, списка тегов (GET).
- ```api/ingredients/``` - Получение, списка ингредиентов (GET).
- ```api/ingredients/<id>``` - Получение ингредиента с соответствующим id (GET).
- ```api/tags/<id>``` - Получение, тега с соответствующим id (GET).
- ```api/recipes/``` - Получение списка с рецептами и публикация рецептов (GET, POST).
- ```api/recipes/<id>``` - Получение, изменение, удаление рецепта с соответствующим id (GET, PUT, PATCH, DELETE).
- ```api/recipes/<id>/shopping_cart/``` - Добавление рецепта с соответствующим id в список покупок и удаление из списка (GET, DELETE).
- ```api/recipes/download_shopping_cart/``` - Скачать файл со списком покупок TXT (в дальнейшем появиться поддержка PDF) (GET).
- ```api/recipes/<id>/favorite/``` - Добавление рецепта с соответствующим id в список избранного и его удаление (GET, DELETE).

#### Операции с пользователями:
- ```api/users/``` - получение информации о пользователе и регистрация новых пользователей. (GET, POST).
- ```api/users/{id}/``` - Получение информации о пользователе. (GET).
- ```api/users/me/``` - получение и изменение данных своей учётной записи. Доступна любым авторизованными пользователям (GET).
- ```api/users/set_password/``` - изменение собственного пароля (PATCH).
- ```api/users/{id}/subscribe/``` - Подписаться на пользователя с соответствующим id или отписаться от него. (GET, DELETE).
- ```api/users/subscribe/subscriptions/``` - Просмотр пользователей на которых подписан текущий пользователь. (GET).

#### Аутентификация новых пользователей:
- ```api/auth/token/login/``` - Получение токена (POST).
- ```api/auth/token/logout/``` - Удаление токена (POST).

#### Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос для регистрации нового пользователя с параметрами
***email username first_name last_name password***
на эндпойнт ```/api/users/```
2. Пользователь отправляет POST-запрос со своими регистрационными данными ***email password*** на эндпоинт ```/api/token/login/``` , в ответе на запрос ему приходит auth-token. 
   Примечание: При взаимодействии с фронтэндом приложения данная операция происходит автоматически при авторизации.

## Ссылки
### Документация API Foodgram:
http://158.160.12.180/api/docs/redoc.html
### Развёрнутый проект:
http://158.160.12.180
http://foodgramyp19.ddns.net

http://foodgramyp19.ddns.net/admin/
http://158.160.12.180/admin/

## Об авторе
- :white_check_mark: [Коломейцев Дмитрий(Certelen)](https://github.com/Certelen)
