from .books import Book
from .utils import TextMatchInfo
from typing import Optional
from pydantic import BaseModel

# Fixed values:
# page = 1; per_page = 25

# NOTE: exempted fields: highlight and highlights
class SearchHits(BaseModel):
  document: Optional[Book] = None
  text_match: Optional[int] = None
  text_match_info: Optional[TextMatchInfo] = None

class SearchBookResults(BaseModel):
  facet_counts: Optional[list] = None
  found: Optional[int] = None
  hits: Optional[list[SearchHits]] = None

# NOTE: current search focuses on book
class Search(BaseModel):
  error: Optional[str] = None
  ids: Optional[list[int]] = None
  page: Optional[int] = None
  per_page: Optional[int] = None
  query_type: Optional[str] = None # GraphQL returns this as "Book" by default but 
  results: Optional[SearchBookResults] = None

# NOTE: for query_type; "Author" is also an appropriate field