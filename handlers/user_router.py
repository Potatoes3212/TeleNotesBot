from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data_base.user_methods import get_user, register_user
from keyboards.reply_other_kb import main_kb

user_router = Router()


# Хендлер команды /start и кнопки "🏠 Главное меню"
@user_router.message(F.text == '🏠 Главное меню')
@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user = await get_user(user_id=message.from_user.id)
    greeting = f"Привет, {message.from_user.full_name}! Выбери необходимое действие"
    if user is None:
        await register_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
        greeting = f"Привет, новый пользователь! Выбери необходимое действие"

    await message.answer(greeting, reply_markup=main_kb())


@user_router.message(F.text == '❌ Остановить сценарий')
async def stop_fsm(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Сценарий остановлен. Для выбора действия воспользуйся клавиатурой ниже",
                         reply_markup=main_kb())
