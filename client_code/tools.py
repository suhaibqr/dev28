import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import base64

# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#


def dict_to_paragraph(data, keys_to_include=None, separator="---"):
    """
    Converts a dictionary or a list of dictionaries into a formatted string.
    For dictionaries, each key-value pair is on a new line, separated by ":".
    For lists of dictionaries, each dictionary's content is separated by a defined separator.

    Skips keys with empty or None values and can filter by a list of keys.

    Args:
        data (dict or list): A single dictionary or a list of dictionaries to convert.
        keys_to_include (list, optional): A list of keys to include in the output. 
                                          Defaults to None (include all keys).
        separator (str, optional): A string used to separate each dictionary's output. 
                                   Defaults to "---".

    Returns:
        str: A formatted string.
    """
    keys_to_include = keys_to_include or []

    def format_dict(single_data):
        """Helper function to format a single dictionary."""
        return '\n'.join(
            f"{key}: {value}" for key, value in single_data.items()
            if (not keys_to_include or key in keys_to_include) and value
        )

    if isinstance(data, dict):
        return format_dict(data)
    elif isinstance(data, list):
        return f"\n{separator}\n".join(format_dict(item) for item in data if isinstance(item, dict))
    else:
        raise ValueError("Input must be a dictionary or a list of dictionaries.")


def decode_base64(encoded_str):
    """
    Decodes a Base64-encoded string and returns the original string.
    
    Parameters:
        encoded_str (str): The Base64-encoded string.
        
    Returns:
        str: The original decoded string.
    """
    try:
        # Decode the Base64 string
        decoded_bytes = base64.b64decode(encoded_str)
        # Convert bytes to string
        original_str = decoded_bytes.decode('utf-8')
        return original_str
    except Exception as e:
        return f"Error decoding Base64 string: {e}"

def encode_to_base64(original_str):
    """
    Encodes a given string into Base64 format.
    
    Parameters:
        original_str (str): The original string to be encoded.
        
    Returns:
        str: The Base64-encoded string.
    """
    try:
        # Convert string to bytes
        original_bytes = original_str.encode('utf-8')
        # Encode bytes to Base64
        base64_bytes = base64.b64encode(original_bytes)
        # Convert Base64 bytes to string
        base64_str = base64_bytes.decode('utf-8')
        return base64_str
    except Exception as e:
        return f"Error encoding to Base64: {e}"