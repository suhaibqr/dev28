from ._anvil_designer import SSH_SESSIONTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class SSH_SESSION(SSH_SESSIONTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  def reset_form(self):
    pass

  def build_form(self,d):
    for k  in d:
      k.update({"hostname":f"{k['address']}:{k['port']}"})

    self.repeating_panel_1.items = d
  
    