from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from logging import basicConfig, INFO
from django.conf import settings

API_TOKEN = settings.TELEGRAM_BOT_TOKEN

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
basicConfig(level=INFO)