from create_bot import logger
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from create_bot import bot
from data_base.dao.repost_dao import add_repost
from keyboards.repost_kb.reply_repost_kb import main_repost_kb
from utils.utils import get_content_info, send_message_user, create_repost_sending_text


add_repost_router = Router()


class AddRepostStates(StatesGroup):
    content = State()  # Ожидаем любое сообщение от пользователя
    check_state = State()  # Финальна проверка

# Handler репостов


@add_repost_router.message(F.text == '🤘🏿 Репосты')
async def start_repost(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ты в меню репостов. Выбери необходимое действие.',
                         reply_markup=main_repost_kb())


@add_repost_router.message(F.forward_origin)
async def start_note(message: Message, state: FSMContext):
    await state.clear()

    # Debug
    # logger.info(f'Получено сообщение: \n{message.model_dump_json(indent=2)}')
    # logger.info(
    #     f"Ссылка на сообщение: \nhttps://t.me/{message.forward_from_chat.username}/{message.forward_from_message_id}")

    content_info = get_content_info(message)

    if content_info.content_type:

        new_repost = await add_repost(user_id=message.from_user.id, origin=content_info.origin, content_type=content_info.content_type,
                                      content_text=content_info.content_text, file_id=content_info.file_id, origin_url=content_info.origin_url, url=content_info.url)

        text = create_repost_sending_text(repost=new_repost, title='Получен репост!')

        await send_message_user(bot=bot, content_type=new_repost.content_type, content_text=text,
                                user_id=message.from_user.id, file_id=new_repost.file_id)

        await message.answer('<b>Репост успешно добавлен!</b>', parse_mode='HTML', reply_markup=main_repost_kb())

    else:
        await message.answer(
            'Я не знаю как работать с таким медафайлом, как ты скинул. Давай что-то другое, ок?'
        )                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
