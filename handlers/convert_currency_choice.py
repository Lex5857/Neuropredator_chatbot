from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboard import make_keyboard
from utils.convert_currency import convert_currency
from config.config import currencies


router = Router()


available_convert = [
    'Курс валюты'
]
available_currency = [
    'Доллар США',
    'Евро',
    'Китайских юаней'
]


class Choice(StatesGroup):
    convert = State()
    currency = State()


@router.message(Command(commands=['valute']))
async def start(message: types.Message, state: FSMContext):
    await message.answer('Официальные курсы валют', reply_markup=make_keyboard(available_convert))
    await state.set_state(Choice.convert)


@router.message(Choice.convert, F.text.in_(available_convert))
async def currency(message: types.Message, state: FSMContext):
    await message.answer('Выберите валюту', reply_markup=make_keyboard(available_currency))
    await state.set_state(Choice.currency)


@router.message(Choice.convert)
async def convert_incorrectly(message: types.Message):
    await message.answer('Неправильно. Попробуйте ещё раз', reply_markup=make_keyboard(available_convert))


@router.message(Choice.currency, F.text.in_(available_currency))
async def currency(message: types.Message, state: FSMContext):
    charCode = currencies[message.text]
    nominal, value = convert_currency(charCode)
    await message.answer(f'{nominal} рубль = {value:.2f}',
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@router.message(Choice.currency)
async def currency_incorrectly(message: types.Message):
    await message.answer('Неправильно. Попробуйте ещё раз', reply_markup=make_keyboard(available_currency))
