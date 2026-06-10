from .books import Book
from .utils import TextMatchInfo
from pydantic import BaseModel

# Fixed values:
# page = 1; per_page = 25

# NOTE: exempted fields: highlight and highlights
class SearchHits(BaseModel):
  document: Book | None = None
  text_match: int | None = None
  text_match_info: TextMatchInfo | None = None

class SearchBookResults(BaseModel):
  facet_counts: list | None = None
  found: int | None = None
  hits: list[SearchHits] | None = None

# NOTE: current search focuses on book
class Search(BaseModel):
  error: str | None = None
  ids: list[int] | None = None
  page: int | None = None
  per_page: int | None = None
  query_type: str | None = None # GraphQL returns this as "Book" by default but
  results: SearchBookResults | None = None

# NOTE: for query_type; "Author" is also an appropriate field
