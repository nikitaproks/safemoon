import requests
import os

from aiogram import types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from misc import dp, bot, BSC_SCAN_API_KEY

from messages import *


class Balance(StatesGroup):
    # waiting_for_food_choice = State()
    waiting_for_wallet_address = State()


def main_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.insert(types.InlineKeyboardButton(
        text='📈Statistics', callback_data='statistics'))
    markup.insert(types.InlineKeyboardButton(
        text='💵Price', callback_data='price'))
    markup.insert(types.InlineKeyboardButton(
        text='🔗Links', callback_data='links'))
    markup.insert(types.InlineKeyboardButton(
        text='📔Token address', callback_data='address'))
    markup.insert(types.InlineKeyboardButton(
        text='💰My SF balance', callback_data='balance'))
    return markup


def trillion_str_convert(stringValue):
    value = round(float(stringValue)/1000000000000, 1)
    outputValue = '{:,} trillion'.format(value)
    return outputValue


def check_response(response):
    print(response.json()['result'])
    if response.json()['status'] == "1":
        reply = trillion_str_convert(response.json()['result'])
    else:
        reply = response.json()['result']
    return reply


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    markup = main_keyboard()
    await bot.send_message(chat_id=message.from_user.id, text=start, reply_markup=markup, parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data == 'price')
async def price(query: types.CallbackQuery):

    markup = main_keyboard()
    await bot.send_message(chat_id=query.from_user.id, text="The price view option is not available yet :(", reply_markup=markup, parse_mode='HTML')


@dp.callback_query_handler(lambda query: query.data == 'statistics')
async def statistics(query: types.CallbackQuery):
    markup = main_keyboard()

    responseTotalSupply = requests.get(
        f"https://api.bscscan.com/api?module=stats&action=tokenCsupply&contractaddress=0xe9e7cea3dedca5984780bafc599bd69add087d56&apikey={BSC_SCAN_API_KEY}")
    responseCirculatingSupply = requests.get(
        f"https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=0xe9e7cea3dedca5984780bafc599bd69add087d56&apikey={BSC_SCAN_API_KEY}")

    totalSupply = check_response(responseTotalSupply)
    circulatingSupply = check_response(responseCirculatingSupply)

    reply = f'<b>Total supply:</b> {totalSupply} \n<b>Circulating Supply:</b> {circulatingSupply}'
    await bot.send_message(chat_id=query.from_user.id, text=reply, reply_markup=markup, parse_mode='HTML')


@ dp.callback_query_handler(lambda query: query.data == 'links')
async def links(query: types.CallbackQuery):
    markup = main_keyboard()
    await bot.send_message(chat_id=query.from_user.id, text=linksSF, reply_markup=markup, parse_mode='HTML')


@ dp.callback_query_handler(lambda query: query.data == 'address')
async def address(query: types.CallbackQuery):
    markup = main_keyboard()
    await bot.send_message(chat_id=query.from_user.id, text=contract, reply_markup=markup, parse_mode='HTML')


@ dp.callback_query_handler(lambda query: query.data == 'balance', state="*")
async def balance(query: types.CallbackQuery):
    await Balance.waiting_for_wallet_address.set()
    await bot.send_message(chat_id=query.from_user.id, text='Please send me your wallet address', parse_mode='HTML')


@ dp.message_handler(state=Balance.waiting_for_wallet_address)
async def balance(message: types.Message, state: FSMContext):
    markup = main_keyboard()
    await state.finish()

    responseWalletBalance = requests.get(
        f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x8076C74C5e3F5852037F31Ff0093Eeb8c8ADd8D3&address={message.text}&tag=latest&apikey={BSC_SCAN_API_KEY}")

    sf = check_response(responseWalletBalance)
    if responseWalletBalance.json() == '1':
        await bot.send_message(chat_id=message.from_user.id, text=f'Your Safe Moon wallet balance is: {sf}', reply_markup=markup, parse_mode='HTML')
    else:
        await bot.send_message(chat_id=message.from_user.id, text=f'{sf}', reply_markup=markup, parse_mode='HTML')


@ dp.message_handler(content_types=types.ContentTypes.ANY)
async def all_other_messages(message: types.Message):
    await message.reply("Sowwy, I'm not able to hold a conversation yet :(", parse_mode='HTML')
