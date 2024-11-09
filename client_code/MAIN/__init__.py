from ._anvil_designer import MAINTemplate
from anvil import *
import anvil.server
from .INVENTORY import INVENTORY
from .DEVICE_DETAILS_SIDE import DEVICE_DETAILS_SIDE

class MAIN(MAINTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.init_forms()
    # Any code you write here will run before the form opens.

  
  def show_device_details(self, data):
    self.sidesheet_content_col.clear()
    self.device_details_form.reset_form()
    self.device_details_form.rebuild_form()
    self.sidesheet_content_col.add_component(self.device_details_form)
    self.layout.show_sidesheet()
    pass

  def init_forms(self):
    self.inventory_form = INVENTORY()
    self.device_details_form = DEVICE_DETAILS_SIDE()
    pass
    