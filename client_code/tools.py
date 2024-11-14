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


# localadmin

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

