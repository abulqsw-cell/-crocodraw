import base64
from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
    InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile, ReplyKeyboardRemove
)
from utils import game_state

router = Router()


@router.message(Command("play"))
async def play(message: types.Message, bot: Bot):
    if game_state.is_game_active():
        await message.answer("⚠️ Сейчас уже кто-то рисует!")
        return

    if message.chat.type in ["group", "supergroup"]:
        bot_info = await bot.get_me()
        # Ссылка для перехода из группы в ЛС
        link = f"https://t.me/{bot_info.username}?start={message.chat.id}"
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎨 Стать художником", url=link)]
        ])
        await message.answer(f"🎮 {message.from_user.first_name} хочет рисовать!", reply_markup=kb)
    else:
        word = game_state.start_game(message.from_user.id, chat_id=message.chat.id)
        # ВАЖНО: ссылка должна быть на GitHub Pages, а не на репозиторий!
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(
                text="🎨 Открыть холст",
                web_app=WebAppInfo(url="https://abulqsw-cell.github.io/-crocodraw/")
            )]],
            resize_keyboard=True
        )
        await message.answer(f"Твое слово: <b>{word}</b>", reply_markup=kb, parse_mode="HTML")


@router.message(lambda message: message.web_app_data)
async def handle_drawing(message: types.Message, bot: Bot):
    raw_data = message.web_app_data.data
    try:
        img_str = raw_data.split(";base64,")[1] if ";base64," in raw_data else raw_data
        image_bytes = base64.b64decode(img_str)
        photo = BufferedInputFile(image_bytes, filename="drawing.png")

        target_chat = game_state.get_target_chat() or message.chat.id
        await message.answer("✅ Отправлено!", reply_markup=ReplyKeyboardRemove())
        await bot.send_photo(target_chat, photo, caption=f"🎨 Рисунок от {message.from_user.first_name}!")
    except Exception:
        await message.answer("Ошибка в рисунке.")


@router.message()
async def guess_handler(message: types.Message):
    if game_state.check_guess(message.text):
        await message.answer(f"🎉 Правильно! Слово: {message.text}")
        game_state.finish_game()