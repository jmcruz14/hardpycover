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
    def __init__(self):
        super().__init__("User does not have access to requested resource.")