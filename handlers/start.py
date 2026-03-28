from aiogram import Router, types, Bot
from aiogram.filters import Command, CommandObject
from handlers.game import play

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject, bot: Bot):
    if command.args:
        # Если пришли из группы, запускаем игру
        await play(message, bot)
    else:
        await message.answer("🎨 Привет! Напиши /play в группе, чтобы начать.")