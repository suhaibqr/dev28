from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ....globals import set_side_panel_data

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item["address"] = self.item["opdevice_ipaddress"] or self.item["DNS_NAME"] or self.item["RESOURCE_URL"] or self.item["DOMAIN_NAME"]
    # Any code you write here will run before the form opens.

  def device_link_click(self, **event_args):
    """This method is called clicked"""
    
    pass

  def device_name_link_click(self, **event_args):
    """This method is called clicked"""
    get_open_form().device_details_sidesheet(self.item)
    pass
