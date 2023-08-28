# Проект Михалыч

Михалыч бот - это бот для телеграм который будет что то делать.

## Установка

1. Клонируйте репозиторий с гит хаб
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Впишите в settings.py переменные:
```
    API_KEY = "Ключ вашего бота"
    PROXY_URL = "URL socks5-прокси"
    PROXY_USERNAME = "Username для авторизации на прокси"
    PROXY_PASSWORD = "Пароль  для авторизации на прокси"
    USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']
```
6. Запустите бота командой `python bot.py`