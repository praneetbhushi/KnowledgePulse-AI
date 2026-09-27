from pydantic import BaseModel


class DocumentSection(BaseModel):
    page: int
    section: str
    text: str