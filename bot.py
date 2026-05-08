import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

load_dotenv()

# Состояния анкеты
class Form(StatesGroup):
    name = State()
    age = State()
    city = State()
    target = State()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Давай создадим твою анкету. Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введи возраст цифрами!")
    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Form.city)

@dp.message(Form.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    kb = [
        [types.KeyboardButton(text="Девушку"), types.KeyboardButton(text="Парня")],
        [types.KeyboardButton(text="Без разницы")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Кого ты хочешь найти?", reply_markup=keyboard)
    await state.set_state(Form.target)

@dp.message(Form.target)
async def process_target(message: types.Message, state: FSMContext):
    data = await state.get_data()
    summary = (
        f"Проверь данные:\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Город: {data['city']}\n"
        f"Ищешь: {message.text}"
    )
    await message.answer(summary, reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
