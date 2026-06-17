'''
    To be deprecated as exceptions will be bundled within each request.
'''

from typing import Any

class GraphQLError(Exception):
    """Custom exception for GraphQL errors"""
    def __init__(self, errors: list, data: Any = None):
        self.errors = errors
        self.data = data
        super().__init__(f"GraphQL errors: {errors}")

class InvalidTokenError(Exception):
    def __init__(self):
        super().__init__("Bearer token invalid/expired.")

class RestrictedAccessError(Exception):
class RateLimitExceededError(Exception):
    def __init__(self, rate_limit: int):
        super().__init__(f"Rate limit of {rate_limit} requests/minute exceeded.")
