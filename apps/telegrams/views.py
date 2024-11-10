from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from asgiref.sync import sync_to_async
from django.conf import settings
import logging

from apps.telegrams.models import TelegramUser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Словарь для хранения последних известных локаций пользователей
user_locations = {}

@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id

    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
        user_id=user_id,
        defaults={
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'user_role': "User"
        }
    )

    if created:
        await message.answer(f"Привет, новый пользователь {message.from_user.full_name}!")
    else:
        await message.answer(f"С возвращением, {message.from_user.full_name}!")

    # Запускаем отправку обновлений локации
    # asyncio.create_task(send_location_updates(user_id, message.chat.id))

async def send_billing(id, billing_source, email, first_name, last_name, phone,
                       payment_code, delivery_from, delivery_to, type_product,
                       length_product, width_product, height_product,
                       weight_product, volume_product, total_price):
    await bot.send_message(-4552009522, f"""Новый лид с {billing_source} #{id}
<b>Имя: </b>{first_name}
<b>Фамилия: </b>{last_name}
<b>Номер: </b>{phone}
<b>Почта: </b>{email}
<b>Код оплаты: </b>{payment_code}
<b>Откуда: </b>{delivery_from}
<b>Куда: </b>{delivery_to}
<b>Вид товара: </b>{type_product}
<b>Длина: </b>{length_product}
<b>Ширина: </b>{width_product}
<b>Высота: </b>{height_product}
<b>Вес товара: </b>{weight_product}
<b>Объем куб: </b>{volume_product}
<b>Итоговая сумма: </b>{total_price}
""")

dp.include_router(router)