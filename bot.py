import asyncio
import logging
import os
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import LinkPreviewOptions, Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

logger = logging.getLogger(__name__)

dp = Dispatcher()

GREET_MESSAGE = (
    "Привет! Отправь мне ссылку на reels из Instagram, а я пришлю ссылку для kkclip.com."
)

UNSUPPORTED_LINK_MESSAGE = (
    "Не получилось распознать эту ссылку. Пришли ссылку на конкретный reels из Instagram."
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        GREET_MESSAGE,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )


@dp.message(F.text)
async def convert_link(message: Message):
    text = message.text if "://" in message.text else f"//{message.text}"
    parsed = urlparse(text)
    host = parsed.netloc.lower()

    if host != "instagram.com" and not host.endswith(".instagram.com"):
        await message.answer(
            GREET_MESSAGE,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
        return

    path_parts = [part for part in parsed.path.split("/") if part]

    match path_parts:
        case ["reel" | "reels", _]:
            pass
        case ["share", "reel", _]:
            pass
        case [_, "reel" | "reels", _]:
            pass
        case _:
            await message.answer(
                UNSUPPORTED_LINK_MESSAGE,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
            return

    preload_link = f"https://www.kkclip.com{parsed.path}"
    logger.info("user=%s converted %r -> %r", message.from_user.id, message.text, preload_link)
    await message.answer(preload_link)


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
