from typing import Optional, Literal, List
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

class LinkType(BaseModel):
    key: str

class Link(BaseModel):
    url: str
    type: LinkType
    title: str

class Identifiers(BaseModel):
    goodreads: Optional[List[str]] = None
    openlibrary: Optional[List[str]] = None
