import anvil.server
from anvil import alert
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#


def say_hello():
  print("Hello, world")


# Client-side code to call the server function
def fetch_inventory_from_bunker(endpoint, query_params, bunker_id ="tdm_vertus"):
    try:
        # Call the server function and get the data
        response_data = anvil.server.call('fetch_inventory_from_bunker', endpoint, query_params, bunker_id)
        
        # Check the status of the response
        if response_data['status'] == 'success':
            return response_data['result']  # Handle the response data (e.g., display it)
        else:
            alert(f"API Call Failed:\n\n{response_data['result']}")
            print("API Call Failed:")
            print(response_data['result'])  # Display the error message
    except Exception as e:
        # Handle any exceptions
        alert(e)