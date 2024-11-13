from ._anvil_designer import NETMIKOTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...automation import remove_from_automation_devices_list, add_to_automation_devices_list,get_automation_devices_list
from anvil_extras import MultiSelectDropDown
from ...globals import netmiko_device_types
from m3._Components import IconButton

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
    name = TextBox(placeholder="Name")
    address = TextBox(placeholder="Address")
    username = TextBox(placeholder="Username")
    password = TextBox(placeholder="Password", hide_text=True)
    port = TextBox(placeholder="Port")
    enable_secret = TextArea(placeholder="EnablePassword")
    device_type = MultiSelectDropDown(enable_filtering= True,multiple= False,enable_select_all=False, placeholder="Platform", width= "70%", items=netmiko_device_types)
    clear = IconButton()
    # delete = 

    
    row = DataRowPanel(item={"address": "ADDRSS","username": None, "password": None,"port": None,"enablesecret": None, "device_type": None})
    row.add_component(address,column="address")
    self.data_grid_copy.add_component(row,index=1)
    # new = get_automation_devices_list()
    # # print(new)
    # for i in new:
    #   new_line = DataRowPanel()
    
    # self.data_grid.add_component(row)
  
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




