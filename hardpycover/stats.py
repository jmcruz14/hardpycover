import re

from collections import defaultdict
from datetime import datetime, date
from typing import Literal, Optional, List


STAT_MAP = {
  "sum_read_count": ("sum", "read_count"),
  "max_review": ("max", "review"),
  "max_review_length": ("max", "review_length"),
  "avg_rating": ("avg", "rating"),
  "avg_read_count": ("avg", "read_count"),
  "avg_review_length": ("avg", "review_length"),
  "sum_review_length": ("sum", "review_length"),
  "sum_likes": ("sum", "likes_count"),
}

def build_time_filter(
  period: Literal["all_time", "year", "month"] = "all_time",
  start_date: str = None,
  end_date: str = None,
  month: str = None,
  year: str = None,
  # start_date
  # end_date
) -> dict:
  _re_parse = re.compile(r"^(?P<Y>\d{4})-?(?P<m>\d{2})-?(?P<d>\d{2})$")

  if end_date is None:
    today: date = date.today()
    end_date: str = today.strftime("%Y-%m-%d")
  else:
    v = _re_parse.match(end_date)
    if not v:
      raise ValueError(f"End date not in ISO 8601 format YYYY-MM-DD: {end_date}")
    v_year = int(v.group("Y"))
    v_month = int(v.group("m"))
    v_day = int(v.group("d"))
    end_date = datetime.date(v_year, v_month, v_day)

  date_condition = {
    "_lte": end_date
  }

  if start_date:
    # do some preconversion shit here
    d = _re_parse.match(start_date)
    if not d:
      raise ValueError(f"Start date not in ISO 8601 format YYYY-MM-DD: {start_date}")


    date_condition.update({"_gte": start_date})

  if period == "all_time":
    return {"date_added": date_condition}

  # NOTE: add use cases for year and month
  # if period == "monthly":
  # if not start_date:
  #   raise ValueError("No start date declared.")
  # if not end_date:
  #   end = today

  # return {
  #   "date"
  # }
  # # NOTE: implement monthly logic wherein range must be defined with a start_date
  # pass

  raise ValueError(
    f"Invalid period '{period}'. Use 'all_time', 'monthly', or 'weekly'."
  )

def select_stat_fields(
  stats: Optional[List[str]] = []
) -> List:

  try:
    STAT_MAP_KEYS = set(STAT_MAP.keys())
    stats_set = set(stats)

    if not stats_set:
      _stats = STAT_MAP
    else:
      _stats = {k: v for k, v in STAT_MAP.items() if k in stats_set}

    # NOTE: probably the funniest way to check if there's an odd one out in the stats_set haha
    if len(stats_set.difference(STAT_MAP_KEYS)) > 0:
      raise ValueError

  except ValueError as e:
    # NOTE: put some error handling here
    print(f"Key not found in stat_map {e}")
    return None
  except Exception as e:
    print(f"Error found: {e}")
    return None


  # ... convert stat_map
  grouped_stats = defaultdict(list)
  for key, (agg_func, field) in _stats.items():
    grouped_stats[agg_func].append(field)

  return  {"aggregate": [{agg_func: fields} for agg_func, fields in grouped_stats.items()]}

def flatten_result(raw: dict, stats: Optional[List[str]] = []) -> dict:
  if not stats:
    stats = list(STAT_MAP.keys())
  stats_set: set = set(stats)
  aggregate: dict = (raw or {}).get("user_books_aggregate").get("aggregate") or {}

  return {
    key: (aggregate.get(agg_func) or {}).get(field)
    for key, (agg_func, field) in STAT_MAP.items()
    if key in stats_set
  }
