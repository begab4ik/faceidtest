from aiohttp import web
from aiohttp_jinja2 import setup, render_template 
from jinja2 import FileSystemLoader
from datetime import datetime
from telegram import Bot
import os

app = web.Application()

# Токен вашего Telegram бота
TELEGRAM_BOT_TOKEN = '6798376566:AAEYDgdzOJNYC_HHwjLe84SRx6NI_NznuQA'

# ID чата, куда будем отправлять фотографии
CHAT_ID = '-4106585257'

# Папка для сохранения фотографий
UPLOAD_FOLDER = 'photos'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Инициализация шаблонизатора Jinja2
setup(app, loader=FileSystemLoader('templates'))  # Убедитесь, что у вас есть папка "templates" с файлом "index.html"

# Маршрут для главной страницы
# Маршрут для главной страницы
async def index(request):
    context = {"message": "Welcome to the photo capture and location sharing page!"}
    return render_template('index.html', request=request, context=context)
app.router.add_static('/static/', path='static', name='static')

# Маршрут для обработки запроса на сделать фото и отправки локации
# Маршрут для обработки запроса на сделать фото и отправки локации
async def take_photo_and_location(request):
    # Получаем изображение из запроса
    data = await request.post()
    photo = data['photo'].file.read()

    # Получаем координаты местоположения из запроса
    latitude = data['latitude']
    longitude = data['longitude']
    
    # Получаем указанное действие (ПРИШЕЛ или УШЕЛ)
    action = data['action']

    # Получаем текущую дату и время
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Формируем текст для отправки в Telegram
    message = f"Date and Time: {current_datetime}\nAction: {action}"

    # Отправляем фотографию и локацию в Telegram бота
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=message)
    await bot.send_location(chat_id=CHAT_ID, latitude=latitude, longitude=longitude)

    # Возвращаем ответ сервера
    return web.Response(text='Success')


# Добавление маршрутов
app.router.add_get('/', index)
app.router.add_post('/take_photo_and_location', take_photo_and_location)

if __name__ == '__main__':
    web.run_app(app)
