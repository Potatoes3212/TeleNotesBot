import asyncio
from pydantic import BaseModel
from typing import Optional, List


class ContentInfo (BaseModel):
    content_type: Optional[str] = None
    file_id: Optional[str] = None
    content_text: Optional[str] = None
    url: Optional[str] = None
    origin: Optional[str] = None
    origin_url: Optional[str] = None
    origin_name: Optional[str] = None
    media_group_id: Optional[str] = None
    media_items: Optional[List[dict]] = None
