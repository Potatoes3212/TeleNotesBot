from create_bot import logger
from data_base.base import connection
from data_base.models import User, Repost
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID


@connection
async def add_repost(session, user_id: int, origin: str,  content_type: str,
                     content_text: Optional[str] = None, file_id: Optional[str] = None, url: Optional[str] = None) -> Optional[Repost]:
    try:
        user = await session.scalar(select(User).filter_by(id=user_id))
        if not user:
            logger.error(f"Пользователь с ID {user_id} не найден.")
            return None

        new_repost = Repost(
            user_id=user_id,
            origin=origin,
            content_type=content_type,
            content_text=content_text,
            file_id=file_id,
            url=url
        )

        session.add(new_repost)
        await session.commit()
        logger.info(
            f"Репост пользователем с ID {user_id} успешно добавлен!")
        return new_repost
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении репоста: {e}")
        await session.rollback()


@connection
async def get_reposts_by_user(session, user_id: int, date_add: str = None, text_search: str = None,
                              content_type: str = None, origin: str = None) -> List[Repost]:
    try:
        result = await session.execute(select(Repost).filter_by(user_id=user_id))
        reposts = result.scalars().all()

        if not reposts:
            logger.info(f"Репосты для пользователя с ID {user_id} не найдены.")
            return []

        # Фильтрация по дате
        if date_add:
            reposts = [
                repost for repost in reposts if repost.created_at.strftime('%Y-%m-%d') == date_add
            ]

        # Фильтрация по текстовому поиску
        if text_search:
            reposts = [
                repost for repost in reposts if text_search.lower() in (repost.content_text or '').lower()
            ]

        # Фильтрация по типу контента
        if content_type:
            reposts = [
                repost for repost in reposts if repost.content_type == content_type
            ]

        # Фильтрация по источнику
        if origin:
            reposts = [
                repost for repost in reposts if origin == repost.origin
            ]

        return reposts
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении репостов: {e}")
        return []


@connection
async def get_repost_by_id(session, repost_id: UUID) -> Optional[Repost]:
    try:
        repost = await session.get(Repost, repost_id)
        if not repost:
            logger.info(f"Репост с ID {repost_id} не найдена.")
            return None

        return repost

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении заметки: {e}")
        return None


@connection
async def get_origins_by_user(session, user_id: int):
    try:
        result = await session.execute(select(Repost.origin).distinct().where(Repost.user_id == user_id))
        reposts_origin = result.scalars().all()
        if not reposts_origin:
            logger.info(f"Нет репостов для пользователя {user_id}")
            return None
        return reposts_origin
    except SQLAlchemyError as e:
        logger.error(f"Ошибка получения источников репостов: {e}")
        return None


@connection
async def delete_repost_by_id(session, repost_id: UUID) -> Optional[Repost]:
    try:
        repost = await session.get(Repost, repost_id)
        if not repost:
            logger.error(f'Репост с ID {repost_id} не найден.')
            return None
        await session.delete(repost)
        await session.commit()
        logger.info(f'Репост с ID {repost_id} успешно удалён.')
        return repost
    except SQLAlchemyError as e:
        logger.error(f'Ошибка удаления репоста: {e}')
        await session.rollback()
        return None
