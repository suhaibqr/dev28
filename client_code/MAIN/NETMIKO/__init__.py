from ._anvil_designer import NETMIKOTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class NETMIKO(NETMIKOTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    b = []
    for i in range(1):
      a={"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None}
      b.append(a)
    self.repeating_panel.items= (b)
    # Any code you write here will run before the form opens.

  def add_row_to_grid_click(self, **event_args):
    """This method is called when the component is clicked."""
    # self.a.append({"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None})
    row = DataRowPanel(item={"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None})
    self.data_grid.add_component(row)
  
    # self.repeating_panel.items.append({"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None})
    pass

  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    pass

  def check_prompt_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    for i in self.repeating_panel.get_components():
      for r in i.get_components():
        if r.__name__ == "TextBox":
          print(r.tag, r.text)
    pass




