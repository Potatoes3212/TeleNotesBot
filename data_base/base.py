from functools import wraps
from sqlalchemy import text

from .database import async_session

def connection(isolation_level=None):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session() as session:
                try:
                    # Устанавливаем уровень изоляции, если передан
                    if isolation_level:
                        await session.execute(text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"))

                    # Выполняем декорированный метод
                    return await method(session=session,*args,  **kwargs)
                except Exception as e:
                    await session.rollback()  # Откатываем сессию при ошибке
                    raise e  # Поднимаем исключение дальше
                finally:
                    await session.close()  # Закрываем сессию

        return wrapper

    return decorator