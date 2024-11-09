from ._anvil_designer import INVENTORYTemplate
from anvil import *
import anvil.server
from ...inventory_fn import fetch_inventory_from_bunker
from ...filter import DictFilter

class INVENTORY(INVENTORYTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_bidinings()
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  def init_binidings(self):
    self.inventory_table = []
    self.inventory_table.filtered_list  = []

  def get_inventory(self):
    user = anvil.server.call("check_auth")
    if not user:
      alert("Not Authenticated")
      return
    data = fetch_inventory_from_bunker("/pmp/resources")
    self.inventory_table = DictFilter(data,[""])
    
      
      

                                       
    