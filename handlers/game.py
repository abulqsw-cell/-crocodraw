from aiogram import Router, types
from aiogram.filters import Command
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from utils import game_state

router = Router()


@router.message(Command("play"))
async def play(message: types.Message, bot: Bot):
    word = game_state.start_game(message.from_user.id)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎨 Рисовать",
            web_app=WebAppInfo(url="https://ТВОЯ_ССЫЛКА")
        )]
    ])

    await message.answer("🎨 Ты рисуешь! Нажми кнопку ниже", reply_markup=kb)

    try:
        await bot.send_message(message.from_user.id, f"Твое слово: {word}")
    except:
        await message.answer("Напиши боту в личку!")

@router.message()
async def guess(message: types.Message, bot: Bot):
    if game_state.check_guess(message.text):
        await message.answer(f"🎉 {message.from_user.first_name} угадал!")

        word = game_state.next_round(message.from_user.id)

        try:
            await bot.send_message(
                message.from_user.id,
                f"Теперь ты рисуешь!\nСлово: {word}"
            )
        except:
            pass



@router.message()
async def get_drawing(message: types.Message):
    if message.web_app_data:
        data = message.web_app_data.data

        await message.answer("🎨 Рисунок получен!")