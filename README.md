# KnigoPoisk - Онлайн библиотека

Django-проект для онлайн-библиотеки KnigoPoisk с системой корзины, списка желаний и отзывов.

## Возможности

- 📚 Каталог книг с фильтрацией по жанрам
- 🛒 Корзина покупок
- ⭐ Список желаний
- 📝 Система отзывов и рейтингов
- 👤 Аутентификация пользователей
- 🔒 Админ-панель для управления контентом

## Технологии

- **Backend**: Django 5.2.9
- **База данных**: PostgreSQL
- **Frontend**: Bootstrap 5
- **Контейнеризация**: Docker + Docker Compose
- **WSGI**: Gunicorn
- **Реверс-прокси**: Nginx
- **CI/CD**: GitHub Actions + GitLab CI

## Установка и запуск

### Локально

1. Клонируйте репозиторий и перейдите в папку проекта:
   ```bash
   git clone <repository-url>
   cd knigopoisk
   ```

2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate  # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Установите PostgreSQL и создайте базу данных:
   ```sql
   CREATE DATABASE knigopoisk;
   CREATE USER user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE knigopoisk TO user;
   ```

5. Откройте `.env` и при необходимости замените секретный ключ:
   ```bash
   nano .env
   ```

6. Выполните миграции и загрузите тестовые данные:
   ```bash
   python manage.py migrate
   python add_sample_data.py
   ```

7. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

8. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

9. Откройте в браузере:
   ```text
   http://127.0.0.1:8000
   ```

### С Docker

1. Запустите контейнеры:
   ```bash
   docker-compose up --build
   ```

2. Откройте приложение:
   ```text
   http://localhost
   ```

## Структура проекта

```
knigopoisk/
├── knigopoisk_project/   # Основные настройки Django
├── accounts/             # Приложение аутентификации
├── books/                # Приложение книг
├── pages/                # Страницы
├── templates/            # HTML-шаблоны
├── .github/              # GitHub Actions workflow
├── Dockerfile            # Образ приложения
├── docker-compose.yml    # Сервисы Docker Compose
├── nginx.conf            # Конфигурация Nginx
├── .gitlab-ci.yml        # CI/CD для GitLab
├── requirements.txt      # Python зависимости
└── .env                  # Переменные окружения
```

## Проверка работоспособности

### Ручная проверка

- Откройте главную страницу
- Пройдите регистрацию
- Войдите в систему
- Добавьте книгу в корзину
- Добавьте книгу в список желаний
- Оставьте отзыв
- Проверьте админку: http://127.0.0.1:8000/admin/

### Автотесты

```bash
source venv/bin/activate
python manage.py test
```

## CI/CD

### GitHub Actions

- Тестирование при push и pull request
- Стадия миграций и тестов

### GitLab CI

- Создан `.gitlab-ci.yml`
- Этапы: `build`, `test`
- Запуск `docker build` и `python manage.py test`

## Важные файлы

- `Dockerfile` — образ контейнера
- `docker-compose.yml` — web + postgres + nginx
- `nginx.conf` — проксирование на `web:8000`
- `.env` — переменные окружения
