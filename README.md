# Flask API Project

## Описание

Это API проект на Flask с использованием Swagger для документации и Docker для контейнеризации. API позволяет управлять постами и комментариями.

## Установка

### Клонирование репозитория

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Pu104ver/project_name.git
   cd yourproject
   ```

### Установка зависимостей

1. Создайте виртуальное окружение и активируйте его:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   Для Windows используйте:

   ```bash
   python -m venv venv
   ```
2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

## Использование

### Локально

1. Запустите сервер:

   ```bash
   FLASK_APP=app.py flask run --host=0.0.0.0
   ```
2. Откройте в браузере:

   ```bash
   http://127.0.0.1:5000/
   ```


### Docker

1. Соберите и запустите контейнеры:

   ```bash
   docker-compose up --build
   ```
2. Откройте в браузере:


## Документация API

Документация доступна по адресу:

```bash
http://127.0.0.1:5000/apidocs/
```

## Тестирование

Запустите тесты:

```bash
pytest
```

## Структура проекта

yourproject/
│
├── data/
│   ├── posts.json
│   ├── comments.json
│   └── ...
│
├── app.py
├── test_app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── ...
# divergent
