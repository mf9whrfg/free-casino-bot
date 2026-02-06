import os
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import database as db
from lexicon import LEXICON

# Берем токен из настроек Koyeb
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    lang, bal = await db.get_user_data(message.from_user.id)
    kb = ReplyKeyboardBuilder()
    # Добавляем кнопки ровно так, как они в словаре
    kb.button(text=LEXICON[lang]['play'])
    kb.button(text=LEXICON[lang]['help'])
    kb.button(text=LEXICON[lang]['lang'])
    kb.adjust(2, 1) # Красивое расположение 2 в ряд и 1 снизу
    
    await message.answer(
        f"{LEXICON[lang]['start']}\n💰 Баланс: {bal}", 
        reply_markup=kb.as_markup(resize_keyboard=True)
    )

# Обработка кнопки "Играть" (учитываем все языки и эмодзи)
@dp.message(F.text.contains("Играть") | F.text.contains("Play") | F.text.contains("Грати") | F.text.contains("Ойнау"))
async def play_menu(message: types.Message):
    await message.answer("🎰 Запускаю слоты...")
    msg = await message.answer_dice(emoji="🎰")
    # Тут позже добавим логику выигрыша из games.py

# Обработка кнопки "Помощь"
@dp.message(F.text.contains("Помощь") | F.text.contains("Help") | F.text.contains("Допомога") | F.text.contains("Көмек"))
async def help_cmd(message: types.Message):
    await message.answer("🆘 Туториал: Нажимай 'Играть', крути слоты и копи монеты! Связь: @твой_ник")

async def main():
    await db.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
