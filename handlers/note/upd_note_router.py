from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from data_base.dao import delete_note_by_id, update_note
from keyboards.reply_note_kb import main_note_kb

from utils.utils import get_content_info

upd_note_router = Router()


class UPDNoteStates(StatesGroup):
    content = State()


@upd_note_router.callback_query(F.data.startswith('dell_note_'))
async def dell_note_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    note_id = call.data.replace('dell_note_', '')
    await delete_note_by_id(note_id=note_id)
    await call.answer(f"Заметка с ID {note_id} удалена!", show_alert=True)
    await call.message.delete()


@upd_note_router.callback_query(F.data.startswith('edit_note_text_'))
async def edit_note_text_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    note_id = call.data.replace('edit_note_text_', '')
    await call.answer(f"Режим редактирования заметки с ID {note_id}")
    await state.update_data(note_id=note_id)
    await call.message.answer(f"Отправь содержимоем для заметки с ID {note_id}")
    await state.set_state(UPDNoteStates.content)


@upd_note_router.message(UPDNoteStates.content)
async def confirm_edit_note_text(message: Message, state: FSMContext):
    content_info = get_content_info(message)
    if content_info.get('content_type'):

        note_id = (await state.get_data()).get('note_id') 
        await update_note(
            note_id=note_id,
            content_text=content_info.get('content_text'),
            content_type=content_info.get('content_type'),
            file_id=content_info.get('file_id'),
            url=content_info.get('url')
        )
        await state.clear()
        await message.answer(f"Заметка с ID {note_id} успешно обновлена!", reply_markup=main_note_kb())

    else:
        await message.answer(
            "Я не знаю как работать с таким медафайлом, как ты скинул. Давай что-то другое, ок?"
        )
        await state.set_state(UPDNoteStates.content)
