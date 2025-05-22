from typing import Any

class GraphQLError(Exception):
    """Custom exception for GraphQL errors"""
    def __init__(self, errors: list, data: Any = None):
        self.errors = errors
        self.data = data
        super().__init__(f"GraphQL errors: {errors}")
