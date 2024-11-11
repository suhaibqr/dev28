from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def delete_click(self, **event_args):
    print(type(self.parent), self.parent)
    # self.remove_from_parent()
    # row = DataRowPanel(item={"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None})
    # self.add_component(row) 
    pass
