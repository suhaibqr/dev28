import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#



def is_valid_tcp_port(port) -> bool:
    """
    Check if the given input is a valid TCP port number.
    Handles both integer and string inputs.

    Args:
        port (Union[int, str]): The port number to validate.

    Returns:
        bool: True if the port is valid, False otherwise.
    """
    try:
        # Convert to integer if it's a string
        port = int(port)
        # Check if it's within the valid range
        return 0 <= port <= 65535
    except (ValueError, TypeError):
        return False