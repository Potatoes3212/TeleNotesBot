from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


# def generate_date_keyboard(notes):
#     unique_dates = {note['date_created'].strftime('%Y-%m-%d') for note in notes}
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[])
#     for date_create in unique_dates:
#         button = InlineKeyboardButton(text=date_create, callback_data=f"date_note_{date_create}")
#         keyboard.inline_keyboard.append([button])

#     keyboard.inline_keyboard.append([InlineKeyboardButton(text="Главное меню", callback_data="main_menu")])

#     return keyboard


# def generate_type_content_keyboard(notes):
#     unique_content = {note['content_type'] for note in notes}
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[])
#     for content_type in unique_content:
#         button = InlineKeyboardButton(text=content_type, callback_data=f"content_type_note_{content_type}")
#         keyboard.inline_keyboard.append([button])

#     keyboard.inline_keyboard.append([InlineKeyboardButton(text="Главное меню", callback_data="main_menu")])

#     return keyboard

def generate_origins_repost_keyboard(origins: List[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for origin in origins:
        button = InlineKeyboardButton(
            text=origin, callback_data=f"repost_origin_{origin}")
        keyboard.inline_keyboard.append([button])

    keyboard.inline_keyboard.append([InlineKeyboardButton(
        text="Главное меню", callback_data="main_menu")])
    
    return keyboard


def main_repost_kb():
    kb_list = [
        [KeyboardButton(text="🙈 Просмотр репостов")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйся меню👇"
    )


def find_repost_kb():
    # kb_list = [
    #     [KeyboardButton(text="📦 Все репосты"), KeyboardButton(text="📅 По дате добавления репоста")],
    #     [KeyboardButton(text="🔍 Поиск по тексту репоста"), KeyboardButton(text="📝 По типу контента репоста")],
    #     [KeyboardButton(text="🌚 По источнику репсота")],
    #     [KeyboardButton(text="🏠 Главное меню")]
    # ]
    kb_list = [
        [KeyboardButton(text="📦 Все репосты")],
        [KeyboardButton(text="🦀 По источнику публикации")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите опцию👇"
    )


def del_repost_kb(repost_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Удалить", callback_data=f"dell_repost_{repost_id}")]])
