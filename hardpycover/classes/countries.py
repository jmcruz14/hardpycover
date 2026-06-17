from pydantic import BaseModel, AfterValidator
from datetime import datetime
from typing import Annotated

from .editions import Edition

# NOTE: explore inclusion of field validator concerning countries included
# like pycountry

def lowercase_codes(code: str) -> str:
  if not code.islower():
    raise ValueError(f"{code} is not in lowercase.")
  return code

def iso_startswith(iso_3166: str) -> str:
  if not iso_3166.startswith("ISO 3166"):
    raise ValueError("ISO 3166 improperly coded")
  return iso_3166
class Country(BaseModel):
  """Represents `Country` schema which pertains to
  the **country of publication**.

  For more information, read the `schema description. <https://docs.hardcover.app/api/graphql/schemas/countries/#what-is-a-country>`_"""

  code2: Annotated[str, AfterValidator(lowercase_codes)] | None = None
  code3: Annotated[str, AfterValidator(lowercase_codes)] | None = None
  created_at: datetime | None = None
  editions: list[Edition] | None = None
  id: int | None = None
  intermediate_region: str | None = None
  intermediate_region_code: str | None = None
  iso_3166: Annotated[str, AfterValidator(iso_startswith)] | None = None
  name: str | None = None
  phone_code: str | None = None
  region: str | None = None
  region_code: str | None = None
  sub_region: str | None = None
  sub_region_code: str | None = None
  updated_at: datetime | None = None

  # NOTE: following may need field validators: intermediate_region
  # intermediate_region_code, iso_3166, phone_code, region_code, region

# TODO: create some kind of book query where code2/code3 is equal to