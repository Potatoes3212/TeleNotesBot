from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from create_bot import bot
from data_base.dao.repost_dao import add_repost
from keyboards.repost_kb.reply_repost_kb import main_repost_kb, find_repost_kb
from keyboards.mode_select_kb import stop_fsm
from utils.utils import get_content_info, send_message_user


add_repost_router = Router()


class AddRepostStates(StatesGroup):
    content = State()  # Ожидаем любое сообщение от пользователя
    check_state = State()  # Финальна проверка

# Handler репостов


@add_repost_router.message(F.text == '🤘🏿 Репосты')
async def start_repost(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ты в меню Репостов. Выбери необходимое действие.',
                         reply_markup=main_repost_kb())


@add_repost_router.message(F.forward_origin)
async def start_note(message: Message, state: FSMContext):
    await state.clear()

    content_info = get_content_info(message)

    if content_info.get('content_type'):
        text = (f"<b>Получен репост</b>\n"
                f"Источник: {content_info['origin']}\n"
                f"Тип: {content_info['content_type']}\n"
                f"Подпись: {content_info['content_text'] if content_info['content_text'] else 'Отсутствует'}\n"
                f"File ID: {content_info['file_id'] if content_info['file_id'] else 'Нет файла'}\n"
                f"Ссылка в сообщении: {content_info['url'] if content_info['url'] else 'Нет ссылки'}")
        await send_message_user(bot=bot, content_type=content_info['content_type'], content_text=text,
                                user_id=message.from_user.id, file_id=content_info['file_id'])

        await add_repost(user_id=message.from_user.id, origin=content_info.get('origin'), content_type=content_info.get('content_type'),
                         content_text=content_info.get('content_text'), file_id=content_info.get('file_id'), url=content_info.get('url'))
        await message.answer('<b>Репост успешно доабвлен!</b>', parse_mode='HTML', reply_markup=main_repost_kb())

    else:
        await message.answer(
            'Я не знаю как работать с таким медафайлом, как ты скинул. Давай что-то другое, ок?'
        )


@add_repost_router.message(AddRepostStates.content)
async def handle_user_note_message(message: Message, state: FSMContext):

    content_info = get_content_info(message)
    if content_info.get('content_type'):
        await state.update_data(**content_info)

        text = (f"Получена заметка:\n"
                f"Тип: {content_info['content_type']}\n"
                f"Подпись: {content_info['content_text'] if content_info['content_text'] else 'Отсутствует'}\n"
                f"File ID: {content_info['file_id'] if content_info['file_id'] else 'Нет файла'}\n"
                f"Ссылка в сообщении: {content_info['url'] if content_info['url'] else 'Нет ссылки'}\n\n"
                f"Все ли верно?")
        await send_message_user(bot=bot, content_type=content_info['content_type'], content_text=text,
                                user_id=message.from_user.id, file_id=content_info['file_id'],
                                kb=main_repost_kb())
        await state.set_state(AddRepostStates.check_state)
    else:
        await message.answer(
            'Я не знаю как работать с таким медафайлом, как ты скинул. Давай что-то другое, ок?'
        )
        await state.set_state(AddRepostStates.content)
