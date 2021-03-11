from misc import dp, bot

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from messages import *


@dp.message_handler(commands=['start'], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(text=start)
