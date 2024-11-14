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
    Handles:
      - Key-value pairs where values can be strings, numbers, lists, or dictionaries.
      - Lists of dictionaries, formatting each dictionary in a readable way.

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

    def format_value(value):
        """Formats values, handling lists and list of dictionaries."""
        if isinstance(value, list):
            if all(isinstance(item, dict) for item in value):
                # Format a list of dictionaries
                return "\n  - " + "\n  - ".join(f"\n{dict_to_paragraph(item)}" for item in value)
            else:
                # Format a list of other types
                return "\n  - " + "\n  - ".join(str(item) for item in value)
        return str(value)

    def format_dict(single_data):
        """Helper function to format a single dictionary."""
        return '\n'.join(
            f"{key}: {format_value(value)}"
            for key, value in single_data.items()
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


def dict_to_yaml_string(data, indent=0):
    """
    Converts a Python dictionary to a YAML-formatted string without external libraries.

    Args:
        data (dict): The dictionary to convert to YAML.
        indent (int): The current indentation level.

    Returns:
        str: YAML string.
    """
    yaml_str = ""
    indentation = "  " * indent
    data = mask_passwords(data)
    if isinstance(data, dict):
        for key, value in data.items():
            yaml_str += f"{indentation}{key}:"
            if isinstance(value, (dict, list)):
                yaml_str += "\n" + dict_to_yaml_string(value, indent + 1)
            else:
                yaml_str += f" {value}\n"
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                yaml_str += f"{indentation}-\n" + dict_to_yaml_string(item, indent + 1)
            else:
                yaml_str += f"{indentation}- {item}\n"
    else:
        yaml_str += f"{indentation}{data}\n"

    return yaml_str


def mask_passwords(data):
    """
    Recursively goes through a dictionary or list (which might be nested) 
    and masks any 'password' key values, keeping only the last three characters visible.
    """
    def mask(value):
        # Mask the value except for the last three characters
        if isinstance(value, str) and len(value) > 3:
            return '*' * (len(value) - 3) + value[-3:]
        return value

    if isinstance(data, dict):
        # Iterate over key-value pairs in a dictionary
        for key, value in data.items():
            if key == 'password':
                # Mask if the key is 'password'
                data[key] = mask(value)
            elif isinstance(value, (dict, list)):
                # Recurse if the value is a dict or a list
                data[key] = mask_passwords(value)
    elif isinstance(data, list):
        # Recurse for each item in the list
        for i in range(len(data)):
            data[i] = mask_passwords(data[i])
            
    return data

