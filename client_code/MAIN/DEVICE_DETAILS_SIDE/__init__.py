from ._anvil_designer import DEVICE_DETAILS_SIDETemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ...tools import  decode_base64, dict_to_yaml_string
from ...globals import get_side_panel_data
from ...inventory_fn import fetch_passwords
from anvil.js.window import navigator
from ...bunkers import get_bunkers_list
from ...data_validation import is_valid_tcp_port
from anvil.js.window import open as open_tab
from ...tools import encode_to_base64
from ...automation import add_to_automation_devices_list, check_if_inside_automation_list,remove_from_automation_devices_list, get_automation_devices_list

class DEVICE_DETAILS_SIDE(DEVICE_DETAILS_SIDETemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.bunkers_list = ["No Bunkers Found"]
    self.init_components(**properties)
    try:
      self.bunkers_list = list(get_bunkers_list().keys())
      self.refresh_data_bindings()
      if self.bunkers_list:
        self.bunkers_dropdown_menu.selected_value = "TDM Vertus"
    except Exception as e:
      pass
    
    
   
    # Any code you write here will run before the form opens.


  def build_details_text(self,data):
    keys_to_include = [
            "RESOURCE_NAME", "RESOURCE_TYPE", "RESOURCE_DESCRIPTION", "DNS_NAME", 
            "DOMAIN_NAME", "RESOURCE_URL", "LOCATION", "opdevicedisplayName", 
            "opdevice_ipaddress", "opdevice_vandorName", "opdevice_deviceName", 
            "opdevice_category", "opdevice_groupDisplayName"
        ]
    
    txt = dict_to_yaml_string(data,keys_to_include=keys_to_include)
    self.device_details_text.text = txt

  def get_pmp_details_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    d = process_data(self.data)
    self.device_details_rep.items = d

  
    

  def reset_form(self):
    self.device_details_rep.items = []
    self.pmp_description.content = ""
    self.device_details_text.text = ""
    self.address_text_box.text = ""
    self.port_text_box.text = ""
    self.username_text_box.text = ""
    self.password_text_box.text = ""
    self.automation_toggle_btn.selected = False
    
  def rebuild_form(self, data):
    self.data = data
    self.build_details_text(self.data)
   
  
  def edit_boxes(self,row):
    # print("DNA_NAME:", self.data["DNS_NAME"], "\n" ,"row:", row)
    self.address_text_box.text = self.data["DNS_NAME"] or self.data["opdevice_ipaddress"] or self.data["RESOURCE_URL"]
    self.port_text_box.text = 22
    self.username_text_box.text = row["ACCOUNT_NAME"]
    self.password_text_box.text = row["PASSWORD"]

  def bunkers_dropdown_menu_change(self, **event_args):
    """This method is called when an item is selected"""
    print("selected bunker value", event_args["sender"].selected_value)
    pass

  def checkport_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    if not all([self.address_text_box.text, is_valid_tcp_port(self.port_text_box.text)]):
      Notification("Make Sure Address, Port, and Bunker are selected").show()
    try:
      r = anvil.server.call("check_port", self.address_text_box.text, self.port_text_box.text)
      if r["status"] == "failed":
        alert(f"Checking Port Failed:\n\n {r['result']}")
      else:
        alert(r["result"])
    except Exception as e:
      alert(f"Ping Faild: {e}")

  def ping_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    if not all([self.address_text_box.text]):
      Notification("Make Sure Address field has a valid address")
    try:
      r = anvil.server.call("ping_host", self.address_text_box.text, self.port_text_box.text)
      if r["status"] == "failed":
        alert(f"Pinging Failed:\n\n {r['result']}")
      else:
        alert(r["result"])
    except Exception as e:
      alert(f"Ping failed: {e}")

  def ssh_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    try:
      token = anvil.server.call("generate_jwt_token")
    except Exception as e:
      alert("Couldnt Get Token")
    bunker = self.bunkers_dropdown_menu.selected_value
    print("get_bunkers_list():", get_bunkers_list())
    print("get(bunker)" , get_bunkers_list().get(bunker))
    print("get_bunkers_list().get(bunker)[1]:", get_bunkers_list().get(bunker)[1])
    bunker = get_bunkers_list().get(bunker)[1]
    hostname = self.address_text_box.text
    username = self.username_text_box.text
    port = self.port_text_box.text
    password = encode_to_base64(self.password_text_box.text)
    if not all([hostname,username,password,port]):
      alert("Make sure address, username, password and port are filled")
    url = f"{bunker}?hostname={hostname}&username={username}&password={password}&port={port}&token={token}"
    print("opening in a new tab", url)
    open_tab(url, "_blank")



  def automation_toggle_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    hostname = self.address_text_box.text
    username = self.username_text_box.text
    port = self.port_text_box.text
    password = encode_to_base64(self.password_text_box.text)
    
    d = {
      "hostname": hostname,
      "username": username,
      "port": port,
      "password": password,
    }
    if not event_args["sender"].selected:
      print("it was seleceted before clicking, we will delete")
      remove_from_automation_devices_list(d)
      return
    else:
      if not check_if_inside_automation_list(d):
        add_to_automation_devices_list(d)
        event_args["sender"].selected = True
    
  
   

def process_data(data):
    # Step 1: Extract "RESOURCE_ID" and "ACCOUNT ID"
    extracted_data = []
    print("data", data)
    
    
    resource_id = data.get("RESOURCE_ID", "")
    accounts = data.get("ACCOUNT_LIST", [])
    for account in accounts:
        extracted_data.append({
            "RESOURCE_ID": resource_id,
            "ACCOUNT_ID": account.get("ACCOUNT ID", "")
        })
    
    # Step 2: Call the fetch_passwords function with the extracted data
    fetched_passwords = fetch_passwords(extracted_data)

    # Step 3: Generate the final list of dictionaries
    result = []
    
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
                "PASSWORD": decode_base64(matching_password_entry.get("PASSWORD", "")),
                "ACCOUNT_DESCRIPTION": account.get("ACCOUNT_DESCRIPTION", "")
            })
    return result

