import asyncio
import logging
import os
import re

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import LinkPreviewOptions, Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

REEL_RE = re.compile(r"instagram\.com/reel/([A-Za-z0-9_-]+)")

logger = logging.getLogger(__name__)

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Отправь мне ссылку на Instagram Reels вида\n"
        "https://www.instagram.com/reel/<ID>/\n"
        "и я пришлю ссылку для kkclip.com.",
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@dp.message(F.text.regexp(REEL_RE, mode="search"))
async def convert_link(message: Message):
    reel_id = REEL_RE.search(message.text).group(1)
    result = f"https://www.kkclip.com/reel/{reel_id}/"
    logger.info("user=%s converted %r -> %r", message.from_user.id, message.text, result)
    await message.answer(result)


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
