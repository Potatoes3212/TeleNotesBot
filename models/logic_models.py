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

    def add_media_item(self, content_type: str, file_id: str) -> None:
        self.media_items.append(
            {
                'content_type': content_type,
                'file_id': file_id
            })

    def get_count_media(self):
        return len(self.media_items)