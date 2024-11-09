from ._anvil_designer import DEVICE_DETAILS_SIDETemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ...tools import dict_to_paragraph
from ...globals import get_side_panel_data
from ...inventory_fn import fetch_passwords

class DEVICE_DETAILS_SIDE(DEVICE_DETAILS_SIDETemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    
    self.init_components(**properties)
    
   
    # Any code you write here will run before the form opens.


  def build_details_text(self,details):
    keys_to_include = [
            "RESOURCE_NAME", "RESOURCE_TYPE", "RESOURCE_DESCRIPTION", "DNS_NAME", 
            "DOMAIN_NAME", "RESOURCE_URL", "LOCATION", "opdevicedisplayName", 
            "opdevice_ipaddress", "opdevice_vandorName", "opdevice_deviceName", 
            "opdevice_category", "opdevice_groupDisplayName"
        ]
    
    txt = dict_to_paragraph(get_side_panel_data(),keys_to_include=keys_to_include)
    self.device_details_text.text(txt)

  def get_pmp_details_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    d = process_data(self.data)
    
    self.device_details_rep.items = d



  def reset_form(self):
    self.device_details_rep = []
    self.pmp_description.clear()
    self.device_details_text.clear()
    self.address_text_box.text = ""
    self.port_text_box.text = ""
    self.username_text_box.text = ""
    self.password_text_box.text = ""
    
  def rebuild_form(self):
    self.build_details_text()
    self.data = get_side_panel_data()


def process_data(data):
    # Step 1: Extract "RESOURCE_ID" and "ACCOUNT ID"
    extracted_data = []
    for item in data:
        resource_id = item.get("RESOURCE_ID", "")
        accounts = item.get("ACCOUNT_LIST", [])
        for account in accounts:
            extracted_data.append({
                "RESOURCE_ID": resource_id,
                "ACCOUNT_ID": account.get("ACCOUNT ID", "")
            })
    
    # Step 2: Call the fetch_passwords function with the extracted data
    fetched_passwords = fetch_passwords(extracted_data)

    # Step 3: Generate the final list of dictionaries
    result = []
    for item in data:
        resource_id = item.get("RESOURCE_ID", "")
        accounts = item.get("ACCOUNT_LIST", [])
        for account in accounts:
            account_id = account.get("ACCOUNT ID", "")
            matching_password_entry = next(
                (entry for entry in fetched_passwords 
                 if entry["RESOURCE_ID"] == resource_id and entry["ACCOUNT_ID"] == account_id),
                None
            )
            if matching_password_entry:
                result.append({
                    "ACCOUNT_NAME": account.get("ACCOUNT NAME", ""),
                    "PASSWORD": matching_password_entry.get("PASSWORD", ""),
                    "ACCOUNT_DESCRIPTION": account.get("ACCOUNT_DESCRIPTION", "")
                })
              
    return result



              # "ACCOUNT_DESCRIPTION": account.get("ACCOUNT_DESCRIPTION", "")