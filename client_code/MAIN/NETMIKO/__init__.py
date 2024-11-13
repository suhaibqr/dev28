from ._anvil_designer import NETMIKOTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...automation import remove_from_automation_devices_list, add_to_automation_devices_list,get_automation_devices_list
from anvil_extras.MultiSelectDropDown import MultiSelectDropDown
from ...globals import netmiko_device_types
from m3._Components.IconButton import IconButton
from ...tools import dict_to_paragraph

class NETMIKO(NETMIKOTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # b = []
    # for i in range(1):
    #   a={"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None}
    #   b.append(a)
    # self.repeating_panel.items= (b)
    # Any code you write here will run before the form opens.

  def add_from_inventory_click(self, **event_args):
    """This method is called when the component is clicked."""
    # self.a.append({"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None})
    print(self.repeating_panel.items)
    if not self.repeating_panel.items or self.repeating_panel.items == []:
      t = get_automation_devices_list()[:]
      self.repeating_panel.items = [*t]
    else:
      self.repeating_panel.items = [*self.repeating_panel.items, *get_automation_devices_list()]

    pass


  def check_prompt_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    devices = []
    if len(self.repeating_panel.get_components()) < 1:
      Notification("No devices in the list").show()
      return

    for i in self.repeating_panel.get_components():
      device = {}
      for r in i.get_components():
        if r.tag == "name":
          device['name'] = r.text
        if r.tag == 'address':
          device['host'] = r.text
        if r.tag == "username":
          device["username"] = r.text
        if r.tag == 'password':
          device["password"] = r.text
        if r.tag == 'port':
          device["port"] = 'port'
        if r.tag == 'secret':
          device['secret'] = r.text
        if r.tag == 'device_type':
          print("found, device_type")
          device['device_type'] = r.selected
        if r.tag == 'is_telnet':
          print("found telnet")
          device['is_telnet'] = r.checked or False
      if not all([device['name'],device['host'], device['username'], device['password'], device['port'], device['device_type'] ]):
        Notification("Name, Address, Username, Password, Port, Device Type: Are Mandatory", title="Some Fields are missing").show()
        return
      # devices.append(device)
    
    alert(f"Will Check the prompt for the following, please confirm:\n{dict_to_paragraph(devices)}", large=True)

        
    


  def add_row_manually_click(self, **event_args):
    """This method is called when the component is clicked."""
    if self.repeating_panel.items:
      self.repeating_panel.items = [*self.repeating_panel.items, {"name": "zzz", "host": None,"username": None, "password": None,"port": None,"secret": None, "device_type": None}]
    else:
      self.repeating_panel.items = [{"name": "zzz", "host": None,"username": None, "password": None,"port": None,"secret": None, "device_type": None}]
    pass

  def text_area_1_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    pass

  def set_run_time_click(self, **event_args):
    """This method is called when the component is clicked."""
    # f = get_open_form()
    # f.sidesheet_content_col.clear()
    # self.sc.reset_form()
    # self.device_details_form.rebuild_form()
    # self.sidesheet_content_col.add_component(self.device_details_form)
    # self.layout.show_sidesheet()
    pass
    
    
    
