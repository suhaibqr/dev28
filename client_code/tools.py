import anvil.server
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#


def dict_to_paragraph(data, keys_to_include=None):
    """
    Converts a dictionary into a string with each key-value pair on a new line,
    separated by ":". Skips keys with empty or None values and can filter by a list of keys.

    Args:
        data (dict): The dictionary to convert.
        keys_to_include (list, optional): A list of keys to include in the output. 
                                          Defaults to None (include all keys).

    Returns:
        str: A formatted string.
    """
    # Use all keys if no specific keys are provided
    keys_to_include = keys_to_include or data.keys()
    
    # Generate the output string
    return '\n'.join(
        f"{key}: {value}" for key, value in data.items()
        if key in keys_to_include and value
    )