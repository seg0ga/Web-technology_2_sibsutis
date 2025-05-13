## VideoHost Documentation

### 1. ОСНОВНЫЕ ВОЗМОЖНОСТИ
- Регистрация и авторизация пользователей
- Загрузка видеофайлов (MP4, MOV, AVI, MKV, WebM)
- Просмотр списка всех видео
- Комментирование видео
- Адаптивный дизайн

### 2. УСТАНОВКА

1. Требования:
- Python 3.7+
- pip

2. Установка:
git clone https://github.com/seg0ga/Web-technology_2_sibsutis

cd videohost

pip install -r requirements.txt

4. Запуск:
flask run

### 3. API СПРАВОЧНИК

[POST] /register
Параметры:
- username (строка)
- email (строка)
- password (строка)

[POST] /login 
Параметры:
- username (строка)
- password (строка)

[GET] /logout

[GET] /posts - список всех видео

[POST] /create
Параметры:
- title (строка)
- text (текст)
- video (файл)

[POST] /post/<int:post_id>/comments
Параметры:
- comment_text (строка)

### 4. СТРУКТУРА ПРОЕКТА

/static
  /css - стили
  /uploads/videos - загруженные видео

/templates - HTML шаблоны

  base.html - базовый шаблон
  
  posts.html - список видео
  
  create.html - форма загрузки
  
  login.html - форма входа
  
  register.html - форма регистрации
  
  comments.html - комментарии

app.py - основной файл приложения

### 5. НАСТРОЙКИ

В app.py можно изменить:
- SECRET_KEY - секретный ключ приложения
- UPLOAD_FOLDER - папка для загрузки видео
- MAX_CONTENT_LENGTH - максимальный размер файла (по умолчанию 100MB)
