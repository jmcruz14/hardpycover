from pydantic import BaseModel
from datetime import datetime

from .editions import Edition

# NOTE: explore inclusion of field validator concerning countries included
# like pycountry

class Country(BaseModel):
  """Represented `Country` schema which pertains to
  the **country of publication**.
  
  For more information, read the `schema description. <https://docs.hardcover.app/api/graphql/schemas/countries/#what-is-a-country>`_"""

  code2: str | None = None
  code3: str | None = None
  created_at: datetime | None = None
  editions: list[Edition] | None = None
  id: int | None = None
  intermediate_region: str | None = None
  intermediate_region_code: str | None = None
  iso_3166: str | None = None
  name: str | None = None
  phone_code: str | None = None
  region: str | None = None
  region_code: str | None = None
  sub_region: str | None = None
  sub_region_code: str | None = None
  updated_at: datetime | None = None

  # NOTE: following may need field validators: code2, code3, intermediate_region
  # intermediate_region_code, iso_3166, phone_code, region_code, region