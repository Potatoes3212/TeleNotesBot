from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from data_base.dao.repost_dao import get_reposts_by_user
from keyboards.repost_kb.reply_repost_kb import main_repost_kb, find_repost_kb
from utils.utils import send_many_notes, send_many_reposts

find_repost_router = Router()


class FindNoteStates(StatesGroup):
    text = State()  # Ожидаем любое сообщение от пользователя


@find_repost_router.message(F.text == '🙈 Просмотр репостов')
async def start_views_noti(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выбери какие заметки отобразить', reply_markup=find_repost_kb())


@find_repost_router.message(F.text == '📦 Все репосты')
async def all_views_reposts(message: Message, state: FSMContext):
    await state.clear()
    all_reposts = await get_reposts_by_user(user_id=message.from_user.id)
    if all_reposts:
        await send_many_reposts(all_reposts, bot, message.from_user.id)
        await message.answer(f'Отправлено репостов: {len(all_reposts)}', reply_markup=main_repost_kb())


@find_repost_router.message(F.text == '📅 По дате добавления')
async def date_views_noti(message: Message, state: FSMContext):
    await state.clear()
    all_notes = await get_reposts_by_user(user_id=message.from_user.id)
    if all_notes:
        await message.answer('На какой день вам отобразить заметки?',
                             reply_markup=generate_date_keyboard(all_notes))
    else:
        await message.answer('У вас пока нет ни одной заметки!', reply_markup=main_note_kb())


@find_repost_router.callback_query(F.data.startswith('date_note_'))
async def find_note_to_date(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    date_add = call.data.replace('date_note_', '')
    all_notes = await get_reposts_by_user(user_id=call.from_user.id, date_add=date_add)
    await send_many_notes(all_notes, bot, call.from_user.id)
    await call.message.answer(f'Все ваши {len(all_notes)} заметок на {date_add} отправлены!',
                              reply_markup=main_note_kb())


@find_repost_router.message(F.text == '📝 По типу контента')
async def content_type_views_noti(message: Message, state: FSMContext):
    await state.clear()
    all_notes = await get_reposts_by_user(user_id=message.from_user.id)
    if all_notes:
        await message.answer('Какой тип заметок по контенту вас интересует?',
                             reply_markup=generate_type_content_keyboard(all_notes))
    else:
        await message.answer('У вас пока нет ни одной заметки!', reply_markup=main_note_kb())


@find_repost_router.callback_query(F.data.startswith('content_type_note_'))
async def find_note_to_content_type(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    content_type = call.data.replace('content_type_note_', '')
    all_notes = await get_reposts_by_user(user_id=call.from_user.id, content_type=content_type)
    await send_many_notes(all_notes, bot, call.from_user.id)
    await call.message.answer(f'Все ваши {len(all_notes)} с типом контента {content_type} отправлены!',
                              reply_markup=main_note_kb())


@find_repost_router.message(F.text == '🔍 Поиск по тексту')
async def text_views_noti(message: Message, state: FSMContext):
    await state.clear()
    all_notes = await get_reposts_by_user(user_id=message.from_user.id)
    if all_notes:
        await message.answer('Введите поисковой запрос. После этого я начну поиск по заметкам. Если в текстовом '
                             'содержимом заметки будет обнаружен поисковой запрос, то я отображу эти заметки')
        await state.set_state(FindNoteStates.text)
    else:
        await message.answer('У вас пока нет ни одной заметки!', reply_markup=main_note_kb())


@find_repost_router.message(F.text, FindNoteStates.text)
async def text_noti_process(message: Message, state: FSMContext):
    text_search = message.text.strip()
    all_notes = await get_reposts_by_user(user_id=message.from_user.id, text_search=text_search)
    await state.clear()
    if all_notes:
        await send_many_notes(all_notes, bot, message.from_user.id)
        await message.answer(f'C поисковой фразой {text_search} было обнаружено {len(all_notes)} заметок!',
                             reply_markup=main_note_kb())
    else:
        await message.answer(f'У вас пока нет ни одной заметки, которая содержала бы в тексте {text_search}!',
                             reply_markup=main_note_kb())
