from typing import Optional, List
from pydantic import BaseModel

class Image(BaseModel):
    id: int
    url: str
    color: str
    width: int
    height: int
    color_name: str

class CachedImage(Image):
    pass

class LinkType(BaseModel):
    key: str

class Link(BaseModel):
    url: str
    type: LinkType
    title: str

class Identifiers(BaseModel):
    goodreads: Optional[List[str] | str] = None
    openlibrary: Optional[List[str] | str] = None

class MatchedTokens(BaseModel):
    matched_tokens: Optional[List[str]] = None
    snippet: Optional[str] = None

class TextMatchInfo(BaseModel):
    best_field_score: Optional[str] = None # String representation of an int value
    best_field_weight: Optional[int] = None
    fields_matched: Optional[int] = None
    num_tokens_dropped: Optional[int] = None
    score: Optional[str] = None
    tokens_matched: Optional[int] = None
    typo_prefix_score: Optional[int] = None