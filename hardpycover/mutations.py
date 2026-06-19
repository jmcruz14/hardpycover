import logging
from sgqlc.types import Variable, Arg, non_null
from sgqlc.operation import Operation, GraphQLErrors
from .schema import (
  update_user_input as UpdateUserInput,
  CreateBookFromPlatformInput,
  mutation_root as Mutation
)
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class Mutations:
  def __init__(self, client, query_limit=50, request_counter=None):
    self._client = client
    self._query_limit = query_limit
    self._request_counter = request_counter

  def _run_mutation(self):
    return Operation(Mutation)

  def _check_rate_limit(self):
    if self._request_counter:
        self._request_counter.check_and_increment()

  def create_book(
    self,
    platform_id: int,
    external_id: str,
    book_id: int = None
  ):
    """
      Creates a new book in the Hardcover database via the `upsert_book`
      mutation operation.

      Args:
        platform_id (int): `Platform` ID based on available platforms
          in Hardcover's database (Note: `platform_id=8` is ISBN)
        external_id (int): string ID value associated with connected
          platform
        book_id (int, Optional): Associated book_id in Hardcover
          if book_id already exists

      Examples:
        TBD

      Returns:
        NewBookIdType (mutation_root or dict)
    """
    # NOTE: platform_id=8 is ISBN
    try:
      self._check_rate_limit()
      op = Operation(Mutation, variables={'book': Arg(non_null(CreateBookFromPlatformInput))})
      mut = op.upsert_book(book=Variable('book'))
      mut.__fields__("id", "errors")
      mut.book.__fields__("id", "slug", "title")
      mut.edition.__fields__("id", "title")

      book_input = {
          "platform_id": platform_id,
          "external_id": external_id,
      }
      if book_id is not None:
          book_input["book_id"] = book_id

      raw = self._client(op, variables={"book": book_input})
      res = op + raw
      return res
    except GraphQLErrors as ex:
      logger.error("GraphQLError: %s" % ex.errors)
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def update_password(
    self,
    current_password: str,
    new_password: str,
    new_password_confirmation: str
  ):
    try:
      self._check_rate_limit()
      op = Operation(Mutation, variables={'user': Arg(non_null(UpdateUserInput))})
      mut = op.update_user(user=Variable('user'))

      # NOTE: Return fields on update
      # NOTE: must specify fields to ensure query doesn't break
      mut.__fields__("id", "errors")
      mut.user.__fields__("email", "username", "updated_at")

      password_input = {
          "current_password": current_password,
          "password": new_password,
          "password_confirmation": new_password_confirmation
      }

      raw = self._client(op, variables={"user": password_input})
      res = op + raw
      return res
    except GraphQLErrors as ex:
      logger.error("GraphQLError: %s" % ex.errors)
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def update_bio(
    self,
    bio: str,
  ):
    try:
      self._check_rate_limit()
      op = Operation(Mutation, variables={'user': Arg(non_null(UpdateUserInput))})
      mut = op.update_user(user=Variable('user'))

      # NOTE: Return fields on update
      # NOTE: must specify fields to ensure query doesn't break
      mut.__fields__("id", "errors")
      mut.user.__fields__("email", "username", "updated_at")

      bio_input = {
          "bio": bio
      }

      raw = self._client(op, variables={"user": bio_input})
      res = op + raw
      return res
    except GraphQLErrors as ex:
      logger.error("GraphQLError: %s" % ex.errors)
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)