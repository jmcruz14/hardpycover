from typing import Type, List, Optional, Any, Dict, Union, get_origin, get_args
from pydantic import BaseModel

# 

AUTO_SELECT_DEPTH = 3 # Max allowable by Hardcover

# class Operation:
# 	def __init__(self, typ=None, name=None, **args):
#     if typ is None:
    

def create_query(
    cls: Type[BaseModel], 
    table_name: str,
    query_name: str = "MyQuery",
    selected_fields: Optional[List[Union[str, Dict[str, List]]]] = None,
    arguments: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Generates a standard, modular (single-table) GraphQL query syntax.

    Args:
        cls: Pydantic BaseModel object
        table_name (str): Reference table from Hardcover API
        query_name (str): Custom query name
        selected_fields: List of field names (str) or nested field specifications (dict)
                       Example: ["id", "title", {"book": ["id", "title"]}]
        arguments (dict): GraphQL arguments like where clauses, filters, etc.
    """
    
    if selected_fields is None:
        selected_fields = list(cls.model_fields.keys())
    
    # Validate and format fields
    fields_str = format_fields(cls, selected_fields)

    # Format arguments if provided
    args_str = ""
    if arguments:
        args_str = f"({format_graphql_args(arguments)})"

    query = f"""query {query_name} {{
      {table_name}{args_str} {{
          {fields_str}
        }}
      }}
    """

    return query


def format_fields(
    cls: Type[BaseModel], 
    selected_fields: List[Union[str, Dict]], 
    indent_level: int = 2) -> str:
    """
    Formats selected fields including nested objects.
    
    Args:
        cls: The Pydantic model class
        selected_fields: List of fields to select
        indent_level: Current indentation level
        
    Returns:
        Formatted fields string
    """
    valid_fields = set(cls.model_fields.keys())
    formatted_fields = []
    indent = "  " * indent_level
    
    for field in selected_fields:
      if isinstance(field, str):
        # Simple field
        if field not in valid_fields:
            raise ValueError(f"Invalid field '{field}' for {cls.__name__}. Valid fields are: {valid_fields}")
        formatted_fields.append(f"{indent}{field}")
      
      elif isinstance(field, dict):
        print('Nested field:', field)
        # Nested field
        for field_name, nested_fields in field.items():
          if field_name not in valid_fields:
            raise ValueError(f"Invalid field '{field_name}' for {cls.__name__}. Valid fields are: {valid_fields}")
            
          # Get the type of the nested field
          field_info = cls.model_fields[field_name]
          field_type = field_info.annotation
          
          # Handle Optional types
          origin = get_origin(field_type)
          if origin is Union:
              # Get the non-None type from Optional[Type]
              args = get_args(field_type)
              field_type = next((arg for arg in args if arg is not type(None)), None)
          
          # Check if it's a list type
          if get_origin(field_type) is list:
              field_type = get_args(field_type)[0]
          
          # Format nested fields if it's a BaseModel
          if isinstance(field_type, type) and issubclass(field_type, BaseModel):
              nested_str = format_fields(field_type, nested_fields, indent_level + 1)
              formatted_fields.append(f"{indent}{field_name} {{")
              formatted_fields.append(nested_str.rstrip())
              formatted_fields.append(f"{indent}}}")
          else:
              # If it's not a BaseModel, just add the field name
              formatted_fields.append(f"{indent}{field_name}")
      
      else:
          raise ValueError(f"Invalid field specification: {field}")

    return "\n".join(formatted_fields)


def format_graphql_args(args: Dict[str, Any]) -> str:
    """
    Formats a dictionary of arguments into GraphQL syntax.
    
    Args:
        args: Dictionary of arguments
        
    Returns:
        Formatted GraphQL arguments string
    """
    formatted_args = []
    
    for key, value in args.items():
        formatted_value = format_graphql_value(value)
        formatted_args.append(f"{key}: {formatted_value}")
    
    return ", ".join(formatted_args)


def format_graphql_value(value: Any) -> str:
    """
    Formats a Python value into GraphQL syntax.
    
    Args:
        value: Python value to format
        
    Returns:
        Formatted GraphQL value string
    """
    if isinstance(value, dict):
        # Handle nested objects
        items = []
        for k, v in value.items():
            formatted_v = format_graphql_value(v)
            items.append(f"{k}: {formatted_v}")
        return "{" + ", ".join(items) + "}"
    elif isinstance(value, list):
        # Handle arrays
        items = [format_graphql_value(item) for item in value]
        return "[" + ", ".join(items) + "]"
    elif isinstance(value, str):
        # String values need quotes
        return f'"{value}"'
    elif isinstance(value, bool):
        # Boolean values
        return "true" if value else "false"
    elif value is None:
        # Null values
        return "null"
    else:
        # Numbers and other types
        return str(value)
