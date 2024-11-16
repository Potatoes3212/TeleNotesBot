from pydantic import BaseModel, Op
from typing import Optional

class ContentInfo (BaseModel):
    content_type: Optional[str] = None
    file_id: Optional[str] = None
    content_text: Optional[str] = None
    url: Optional[str] = None
    origin: Optional[str] = None
    origin_url: Optional[str] = None
