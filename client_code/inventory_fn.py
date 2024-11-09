import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from anvil import alert
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#


# Client-side function to fetch inventory from a bunker
def fetch_inventory_from_bunker(bunker_id="tdm_vertus"):
    """
    Calls the server function to fetch inventory data and handles the response.

    Args:
        endpoint (str): The API endpoint to call.
        query_params (dict): Query parameters for the API request.
        bunker_id (str): The bunker ID (default: 'tdm_vertus').

    Returns:
        Any: The response data if the call is successful. None if there's an error.
    """
    try:
        # Call the server function
        response_data = anvil.server.call(
           "fetch_inventory_from_bunker", bunker_id
        )

        # Handle response based on status
        if response_data.get('status') == 'success':
            transform_to_dict = response_data.get('result')
            return  transform_to_dict
        else:
            error_message = response_data.get('result', 'Unknown error occurred.')
            alert(f"API Call Failed:\n\n{error_message}")
            print(f"API Call Failed: {error_message}")  # Log error for debugging
            return None  # Explicitly return None for clarity

    except Exception as e:
        # Handle unexpected exceptions
        alert(f"Unexpected Error: {str(e)}")
        print(f"Unexpected Error: {str(e)}")

    return None  # Return None in case of an error



def transform_to_dict(data_structure):
    """
    Transforms a data structure with fields and data into a list of dictionaries.
    
    Parameters:
        data_structure (dict): A dictionary containing 'fields' and 'data'.
            - fields (list): A list of keys for the dictionary.
            - data (list of lists): A list of lists representing the data.
    
    Returns:
        list: A list of dictionaries where each dictionary maps the fields to the corresponding data values.
    """
    fields = data_structure.get('fields', [])
    data = data_structure.get('data', [])
    
    if not fields or not isinstance(data, list):
        raise ValueError("Invalid data structure. Ensure 'fields' is a list and 'data' is a list of lists.")
    
    # Generate list of dictionaries
    dict_list = [dict(zip(fields, values)) for values in data]
    
    return dict_list





def fetch_passwords(resource_accounts):
    # Example input data
    # resource_accounts = [
    #     {"RESOURCE_ID": "123", "ACCOUNT_ID": "abc"},
    #     {"RESOURCE_ID": "456", "ACCOUNT_ID": "def"},
    # ]
    
    try:
        # Call the server function
        response = anvil.server.call('fetch_passwords_from_api', resource_accounts)
        
        if response['status'] == 'success':
            print("Passwords fetched successfully!")
            print(response['result'])
        else:
            print("Failed to fetch passwords.")
            print(response['result'])
    
    except anvil.server.AnvilError as e:
        print(f"Anvil error: {str(e)}")