import json
import asyncio
from create_bot import logger
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from decouple import config

from create_bot import bot
from data_base.models import Repost
from models.logic_models import ContentInfo
from data_base.dao.repost_dao import add_repost
from keyboards.repost_kb.reply_repost_kb import main_repost_kb
from utils.utils import get_content_info, send_message_user, create_repost_sending_text, send_repost_user


timers = {}

add_repost_router = Router()


class AddRepostStates(StatesGroup):
    content = State()  # Ожидаем любое сообщение от пользователя
    check_state = State()  # Финальна проверка


@add_repost_router.message(F.text == '🤘🏿 Репосты')
async def start_repost(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ты в меню репостов. Выбери необходимое действие.',
                         reply_markup=main_repost_kb())


@add_repost_router.message((F.forward_origin) & (F.media_group_id))
async def take_mg_repost(message: Message, state: FSMContext):
    data = await state.get_data()
    logger.info(
        f'data from state = {json.dumps(data.get("repost", {}), ensure_ascii=False, indent=4)}')

    media_group_id = data.get('repost', {}).get('media_group_id')
    logger.info(f'media_group_id from state {media_group_id}')

    if not media_group_id:
        await state.clear()
        content_info = get_content_info(message)

        logger.info(f'content_info created: {content_info.model_dump_json()}')
        await state.update_data(repost=content_info.model_dump())

    elif message.media_group_id != media_group_id:
        await state.clear()

    elif media_group_id == message.media_group_id:
        content_info = get_content_info(message)

        saved_repost = ContentInfo(**data['repost'])
        saved_repost.add_media_item(
            content_type=content_info.content_type, file_id=content_info.file_id)

        if message.chat.id in timers:
            timers[message.chat.id].cancel()

        task = asyncio.create_task(
            save_media_group(message=message, state=state))
        timers[message.chat.id] = task
        logger.info(f'Текущий таймер: {timers}')

        await state.update_data(repost=saved_repost.model_dump())
        updated_data = await state.get_data()
        logger.info(
            f'state: {json.dumps(updated_data.get("repost", {}), ensure_ascii=False, indent=4)}')


async def save_media_group(message: Message, state: FSMContext):
    await asyncio.sleep(config('GROUP_TIMEOUT', cast=int))
    data = await state.get_data()
    saved_repost = ContentInfo(**data['repost'])

    try:
        new_repost = await save_repost_to_db(user_id=message.from_user.id, content_info=saved_repost)

        logger.info(
            f'Сохранён репост с медиа группой {new_repost.id}')

    except Exception as e:
        logger.error(f'Ошибка вызова save_repost_to_db: {e}')

    await state.clear()
    del timers[message.chat.id]  # Удаление таймера после выполнения

    try:
        await send_accept_message(new_repost)
        await message.answer(f'<b>Репост с {len(new_repost.media)} медиа успешно добавлен!</b>', parse_mode='HTML', reply_markup=main_repost_kb())

    except Exception as e:
        logger.error(f'При отпрвке подтверждающего сообещния: {e}')
    logger.info(f'Процессинг репоста: {new_repost.id} завершён.')


async def save_repost_to_db(user_id: int, content_info: ContentInfo) -> Repost:

    try:
        new_repost = await add_repost(user_id=user_id, origin_name=content_info.origin_name, origin=content_info.origin, content_type=content_info.content_type,
                                      content_text=content_info.content_text, file_id=content_info.file_id, origin_url=content_info.origin_url, url=content_info.url, media=content_info.media_items)
        return new_repost

    except Exception as e:
        logger.error(f'Ошибка сохаранения: {e}')


async def send_accept_message(new_repost: Repost):
    caption = create_repost_sending_text(
        new_repost, title=f'Получен репост c медиа группой!')
    await send_repost_user(bot=bot, repost=new_repost, caption=caption)


@add_repost_router.message((F.forward_origin) & (~F.media_group_id))
async def take_repost(message: Message, state: FSMContext):
    content_info = get_content_info(message)

    if content_info.content_type:

        new_repost = await save_repost_to_db(user_id=message.from_user.id, content_info=content_info)

        text = create_repost_sending_text(
            repost=new_repost, title='Получен репост!')

        await send_message_user(bot=bot, content_type=new_repost.content_type, content_text=text,
                                user_id=message.from_user.id, file_id=new_repost.file_id)

        await message.answer('<b>Репост успешно добавлен!</b>', parse_mode='HTML', reply_markup=main_repost_kb())

    else:
        await message.answer(
            'Я не знаю как работать с таким медафайлом, как ты скинул. Давай что-то другое, ок?'
        )
