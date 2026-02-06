import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon import LEXICON
import database as db

TOKEN = "8330528237:AAExVDZ60O2T-EHZAl0TxsmVrKGya2LPjbY"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    lang, bal = await db.get_user_data(message.from_user.id)
    kb = ReplyKeyboardBuilder()
    for btn in [LEXICON[lang]['play'], LEXICON[lang]['help'], LEXICON[lang]['lang']]:
        kb.button(text=btn)
    await message.answer(f"{LEXICON[lang]['start']}\n💰 Баланс: {bal}", reply_markup=kb.as_markup(resize_keyboard=True))

@dp.message(F.text.in_(['Язык 🌐', 'Language 🌐', 'Мова 🌐', 'Тіл 🌐']))
async def change_lang(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Русский 🇷🇺", callback_data="set_ru")
    kb.button(text="English 🇺🇸", callback_data="set_en")
    kb.button(text="Українська 🇺🇦", callback_data="set_uk")
    kb.button(text="Қазақша 🇰🇿", callback_data="set_kk")
    await message.answer("Выберите язык / Select language:", reply_markup=kb.as_markup())

@dp.callback_query(F.data.startswith("set_"))
async def set_language(callback: types.CallbackQuery):
    new_lang = callback.data.split("_")[1]
    await db.update_lang(callback.from_user.id, new_lang)
    await callback.answer("Готово / Done")
    await callback.message.answer("Язык изменен! Введите /start")

async def main():
    await db.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

