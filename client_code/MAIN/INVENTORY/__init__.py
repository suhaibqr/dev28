from ._anvil_designer import INVENTORYTemplate
from anvil import *
import anvil.server
import .

class INVENTORY(INVENTORYTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.



  def get_inventory(self):
    pmp_api_key = anvil.server.call("get_settings", "pmp_api_key")
    if not pmp_api_key:
      alert("missing or incorrect settings, make sure you have saved your PMP key or report the issue")
    data = anvil.server.call("")      
    