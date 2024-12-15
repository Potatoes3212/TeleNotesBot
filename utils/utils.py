import asyncio
import re

from aiogram import Bot
from aiogram.types import Message, InputMediaAudio, InputMediaVideo, InputMediaDocument, InputMediaPhoto
from typing import Optional
from keyboards.note_kb.reply_note_kb import rule_note_kb
from keyboards.repost_kb.reply_repost_kb import del_repost_kb
from models.logic_models import ContentInfo
from operator import attrgetter
from create_bot import logger
from data_base.models import Repost


def transform_string(input_string):
    # Разделяем строку по запятым
    words = input_string.split(',')
    # Убираем лишние пробелы, приводим к нижнему регистру и заменяем множественные пробелы на один
    cleaned_words = [re.sub(' +', ' ', word.strip().lower())
                     for word in words if word.strip()]
    # Объединяем слова обратно в строку через запятую
    result = ','.join(cleaned_words)
    return result


def get_content_info(message: Message):

    content_type = None
    file_id = None
    content_text = message.text or message.caption
    url = get_url(message)
    media_group_id = None

    if message.photo:
        content_type = "photo"
        file_id = message.photo[-1].file_id
    elif message.video:
        content_type = "video"
        file_id = message.video.file_id
    elif message.audio:
        content_type = "audio"
        file_id = message.audio.file_id
    elif message.document:
        content_type = "document"
        file_id = message.document.file_id
    elif message.voice:
        content_type = "voice"
        file_id = message.voice.file_id
    elif message.text:
        content_type = "text"

    # Получние истоничка репоста
    if message.forward_from_chat and message.forward_from_chat.title:
        origin = message.forward_origin.chat.title
        origin_name = message.forward_from_chat.username
    else:
        origin = None

    if message.media_group_id:
        media_group_id = message.media_group_id

    # Получение сслыки на оригинал репоста
    if message.forward_from_chat and message.forward_from_chat.username and message.forward_from_message_id:
        origin_url = f"https://t.me/{message.forward_from_chat.username}/{message.forward_from_message_id}"
    else:
        origin_url = None

    content_info = ContentInfo(
        content_type=content_type,
        file_id=file_id,
        content_text=content_text,
        url=url, origin=origin,
        origin_url=origin_url,
        origin_name=origin_name,
        media_group_id=media_group_id,
        media_items=[{'content_type': content_type, 'file_id': file_id}]
    )

    return content_info


def get_url(message: Message) -> str | None:
    # Проверка, содержит ли сообщение URL среди entities
    entities = message.entities if message.text else message.caption_entities
    if entities:
        for entity in entities:
            if entity.type == "url":
                text = message.text or message.caption
                # URL из текста
                return text[entity.offset: entity.offset + entity.length]
            elif entity.type == "text_link" and entity.url:
                return entity.url  # Прямой URL из text_link
    return None


async def send_message_user(bot: Bot, user_id, content_type, content_text=None, file_id=None, kb=None):
    if content_type == 'text':
        await bot.send_message(chat_id=user_id, text=content_text, parse_mode='HTML', reply_markup=kb)
    elif content_type == 'photo':
        await bot.send_photo(chat_id=user_id, photo=file_id, caption=content_text, parse_mode='HTML', reply_markup=kb)
    elif content_type == 'document':
        await bot.send_document(chat_id=user_id, document=file_id, caption=content_text, parse_mode='HTML', reply_markup=kb)
    elif content_type == 'video':
        await bot.send_video(chat_id=user_id, video=file_id, caption=content_text, parse_mode='HTML', reply_markup=kb)
    elif content_type == 'audio':
        await bot.send_audio(chat_id=user_id, audio=file_id, caption=content_text, parse_mode='HTML', reply_markup=kb)
    elif content_type == 'voice':
        await bot.send_voice(chat_id=user_id, voice=file_id, caption=content_text, parse_mode='HTML', reply_markup=kb)


async def send_repost_user(bot: Bot, repost: Repost, caption: str, kb=None):

    media = []

    for idx, item in enumerate(repost.media):
        content_type = item['content_type']
        file_id = item['file_id']

        if content_type == 'photo':
            media.append(InputMediaPhoto(
                media=file_id, caption=caption if idx == 0 else None, parse_mode='HTML'))
        elif content_type == 'document':
            media.append(InputMediaDocument(
                media=file_id, caption=caption if idx == 0 else None, parse_mode='HTML'))
        elif content_type == 'video':
            media.append(InputMediaVideo(
                media=file_id, caption=caption if idx == 0 else None, parse_mode='HTML'))
        elif content_type == 'audio':
            media.append(InputMediaAudio(
                media=file_id, caption=caption if idx == 0 else None, parse_mode='HTML'))
    await bot.send_media_group(chat_id=repost.user_id, media=media)
    # await bot.send_message(chat_id=repost.user_id, text="Выбери действие:", reply_markup=kb)


async def send_many_notes(all_notes, bot, user_id):
    for note in all_notes:
        try:
            await send_message_user(bot=bot, content_type=note['content_type'],
                                    content_text=note['content_text'],
                                    user_id=user_id,
                                    file_id=note['file_id'],
                                    kb=rule_note_kb(note['id']))
        except Exception as E:
            print(f'Error: {E}')
            await asyncio.sleep(2)
        finally:
            await asyncio.sleep(0.5)


async def send_many_reposts(all_reposts, bot, user_id):

    all_reposts.sort(key=attrgetter('created_at'))

    for repost in all_reposts:
        logger.info(f'{repost.created_at}: {type(repost.created_at)}')
        try:
            await send_message_user(bot=bot, content_type=repost.content_type,
                                    content_text=create_repost_sending_text(
                                        repost=repost),
                                    user_id=user_id,
                                    file_id=repost.file_id,
                                    kb=del_repost_kb(repost.id))
        except Exception as E:
            print(f'Error: {E}')
            await asyncio.sleep(2)
        finally:
            await asyncio.sleep(0.5)


def create_repost_sending_text(repost: Repost, title: Optional[str] = None) -> str:

    text = []

    if title:
        text.append(f'<b>{title}</b>')

    if repost.origin:
        text.append(f'<b>Источник:</b> {repost.origin}')

    if repost.origin_url:

        text.append(
            f'<a href="{repost.origin_url}">Ссылка на оригинальный пост</a>')

    if repost.content_text:

        content_text = repost.content_text

        if len(content_text) > 600:
            content_text = content_text[:600] + "...\nполный текст в источнике"

        text.append(f"<b>Подпись:</b> \n{content_text}")

    if repost.url:
        text.append(f"<b>Ссылка в сообщении:</b> {repost.url}")

    text.append(
        f"<b>Дата сохранения репоста: {repost.created_at.strftime('%Y-%m-%d') }</b>")

    return '\n'.join(text)
