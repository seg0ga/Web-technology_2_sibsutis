# Видеохостинг на Flask

## Описание проекта

Веб-приложение для загрузки и просмотра видео, реализованное с использованием Flask. Пользователи могут регистрироваться, входить в систему, загружать видео и оставлять комментарии.

---

## Структура проекта

```
Videohost/
├── app.py                # Основной файл приложения Flask
├── instance/
│   └── videohost.db      # База данных SQLite
├── static/
│   ├── css/              # Стили CSS
│   ├── img/              # Изображения
│   └── uploads/videos/   # Загруженные видео
├── templates/            # HTML-шаблоны Jinja2
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── create.html
│   ├── comments.html
│   └── posts.html
```

---

## Установка и запуск

```bash
git clone https://github.com/seg0ga/Web-technology_2_sibsutis
cd Videohost
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
python app.py
```

---

## Зависимости (requirements.txt)

```
Flask
Werkzeug
Jinja2
itsdangerous
click
Flask_SQLAlchemy
```

---

## Аутентификация

### Регистрация

**POST** `/register`

**Форма:** `username`, `password`

**Пример запроса:**
```bash
curl -X POST http://localhost:5000/register \
     -d "username=alice&password=1234"
```

### Вход

**POST** `/login`

**Форма:** `username`, `password`

**Пример запроса:**
```bash
curl -X POST http://localhost:5000/login \
     -d "username=alice&password=1234"
```

---

## Загрузка видео

**POST** `/create`

**Форма:** `title`, `description`, `file (video/mp4)`

**Пример (cURL):**
```bash
curl -X POST http://localhost:5000/create \
     -F "title=My Video" \
     -F "description=Test upload" \
     -F "file=@video.mp4"
```

---

## Просмотр видео

**GET** `/posts`

Возвращает список всех загруженных видео.

---

## Комментарии

**GET** `/comments/<video_id>`

Показать комментарии к видео.

**POST** `/comments/<video_id>`

Добавить комментарий к видео.

**Форма:** `content`

---

## Используемые технологии

- **Flask** — серверное приложение
- **Jinja2** — шаблонизатор HTML
- **SQLite** — встроенная БД
- **HTML/CSS** — интерфейс
- **Bootstrap** — стилизация (опционально)
- **JavaScript** — валидация форм (опционально)

---

## Примечания

- Все загруженные видео хранятся в `static/uploads/videos/`.
- Данные пользователей и видео сохраняются в `instance/videohost.db`.
- Для использования в продакшене рекомендуется добавить авторизацию по токенам и валидацию видеофайлов.
