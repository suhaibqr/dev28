from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from anvil.js.window import navigator


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.activate_description_btn()
    # Any code you write here will run before the form opens.

  def device_details_link_click(self, **event_args):
    """This method is called clicked"""
    f = get_open_form()
    f.device_details_form.edit_boxes(self.item)
    pass


  def activate_description_btn(self):
    if self.item["ACCOUNT_DESCRIPTION"]:
      self.description_btn.enabled = True
    else:
      self.description_btn.enabled = False

  def description_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    get_open_form().device_details_form.pmp_description.content = self.item["ACCOUNT_DESCRIPTION"]
    pass

  def copy_password_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    navigator.clipboard.writeText(self.item["PASSWORD"])
    Notification("Copied to clipboard", timeout=2).show()
   
 