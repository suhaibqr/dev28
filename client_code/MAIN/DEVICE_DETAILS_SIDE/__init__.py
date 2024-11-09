from ._anvil_designer import DEVICE_DETAILS_SIDETemplate
from anvil import *
import anvil.server
from ...tools import dict_to_paragraph
from ...globals import get_side_panel_data

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
    anvil.server.call()
    pass


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