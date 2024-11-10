from typing import Any, Optional
from django.core.management.base import BaseCommand

import apps.telegrams.views


class Command(BaseCommand):
    help = "Start Bot Aiogram"

    def handle(self, *args: Any, **options: Any) -> str | None:
        print("START BOT")
        apps.telegrams.views.dp.run_polling(apps.telegrams.views.bot)