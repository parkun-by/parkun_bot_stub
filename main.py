import logging
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ParseMode
from aiogram.utils import executor
import aiohttp

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    cat_button = types.InlineKeyboardButton(
        text='Очень жаль, покажите кота',
        callback_data='/gimme_cat')

    keyboard.add(cat_button)

    await bot.send_message(message.chat.id,
                           config.WELCOME_TEXT,
                           reply_markup=keyboard,
                           disable_web_page_preview=True)


@dp.callback_query_handler(lambda call: call.data == '/gimme_cat', state='*')
async def gimme_cat_pressed(call, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    cat_button = types.InlineKeyboardButton(
        text='Еще',
        callback_data='/gimme_cat')

    keyboard.add(cat_button)

    if url := await get_cat_url():
        await bot.send_message(chat_id=call.message.chat.id,
                               text=f'<a href="{url}">meow</a>',
                               reply_markup=keyboard,
                               parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(call.message.chat.id,
                               "🐈",
                               reply_markup=keyboard)

    await bot.answer_callback_query(call.id)


async def get_cat_url() -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(config.CAT_URL) as response:
                resp_json = await response.json(content_type=None)
                return resp_json[0]["url"]

    except Exception:
        return None


@dp.message_handler(content_types=types.ContentTypes.ANY, state='*')
async def empty_state(message: types.Message):
    await welcome(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
