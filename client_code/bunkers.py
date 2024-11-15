import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

# bunkers_list = {"TDM": ["link1", "link2"],"WPG": ["link3", "link4"]}

bunkers_list = {
    'TDM Vertus': ['https://devtest.tdmgroup.net:8000',
                   'https://devtest.tdmgroup.net:8888'],
    'Bunker_2': ['https://10.215.10.215:8000', 'https://10.215.10.215:8888'],
    'Bunker_3': ['https://10.215.10.215:8000', 'https://10.215.10.215:8888']
    # Add more bunker IDs and base URLs as needed
}


# def get_bunkers_list():
#   global bunkers_list
#   if bunkers_list:
#     return bunkers_list
#   else:
#     try:
#       bunkers_list = anvil.server.call("get_bunkers_list")
#       return bunkers_list
#     except Exception as e:
#       # alert(f"Failed to get bunkers list: {e}")
#       return [{"No Bunkers Found": "No Bunkers Found"}]

def get_bunkers_list():
  return bunkers_list