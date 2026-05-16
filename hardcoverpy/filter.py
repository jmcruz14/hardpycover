def get_critical_book_fields(
  entry: list[dict],
  essential_fields: list = [
    "author_names",
    "has_audiobook",
    "has_ebook",
    "title", 
    "rating",
    "pages",
    "release_date",
    "release_year",
    "users_count", 
    "users_read_count"
  ]
):
  """Filters out non-critical `Book` fields from a list of `Book` objects.

  Args:
    entry (list(dict)): Iterable list of dictionary fields that are of `Book` type. 
    essential_fields (list): Iterable list of declared fields.

  Returns:
    book_object (dict): Updated book object.
  """


  document = entry["document"]
  return {"document": {key: document[key] for key in essential_fields if key in document}}