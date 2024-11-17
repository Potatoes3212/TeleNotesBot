from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from data_base.dao.repost_dao import get_reposts_by_user, get_origins_by_user
from keyboards.repost_kb.reply_repost_kb import main_repost_kb, find_repost_kb, generate_origins_repost_keyboard
from utils.utils import send_many_reposts

find_repost_router = Router()


class FindNoteStates(StatesGroup):
    text = State()  # Ожидаем любое сообщение от пользователя


@find_repost_router.message(F.text == '🙈 Просмотр репостов')
async def start_views_noti(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выбери какие репосты отобразить', reply_markup=find_repost_kb())


@find_repost_router.message(F.text == '📦 Все репосты')
async def all_views_reposts(message: Message, state: FSMContext):
    await state.clear()
    all_reposts = await get_reposts_by_user(user_id=message.from_user.id)
    if all_reposts:
        await send_many_reposts(all_reposts, bot, message.from_user.id)
        await message.answer(f'Отправлено репостов: {len(all_reposts)}', reply_markup=main_repost_kb())
    else:
        await message.answer('У вас пока нет репостов.', reply_markup=main_repost_kb())


# Поиск по источнику репоста
@find_repost_router.message(F.text == '🦀 По источнику публикации')
async def wievs_origin_reposts(message: Message, state: FSMContext):
    await state.clear()
    all_reposts_origin = await get_origins_by_user(user_id=message.from_user.id)
    if all_reposts_origin:
        await message.answer('От какого источника вы хотите получить репосты?',
                             reply_markup=generate_origins_repost_keyboard(all_reposts_origin))
    else:
        await message.answer(text='У тебя пока нет репостов', reply_markup=main_repost_kb())


@find_repost_router.callback_query(F.data.startswith('repost_origin_'))
async def defwievs_reposts_by_origin(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    origin = call.data.replace('repost_origin_', '')
    reposts_by_origin = await get_reposts_by_user(
        user_id=call.from_user.id, origin=origin)
    await send_many_reposts(reposts_by_origin, bot, call.from_user.id)
    await call.message.answer(text=f'Отправлены все репосты от автора:\n"{origin}"\nВсего репостов: {len(reposts_by_origin)}', reply_markup=main_repost_kb())
