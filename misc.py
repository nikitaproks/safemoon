import logging
import os

from dotenv import load_dotenv, find_dotenv

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv(find_dotenv())

TOKEN = os.environ['TOKEN']
#TOKEN = os.environ['TEST_TOKEN']

BSC_SCAN_API_KEY = os.environ['BSC_SCAN_API_KEY']

WEBHOOK_HOST = 'https://safemoonbot.herokuapp.com'
#WEBHOOK_HOST = "https://468ddd420a3f.ngrok.io"
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')


# common
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)
