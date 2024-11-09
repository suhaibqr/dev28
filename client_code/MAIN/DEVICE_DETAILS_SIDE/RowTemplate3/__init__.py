from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def device_details_link_click(self, **event_args):
    """This method is called clicked"""
    anvil.server.call()
    pass
