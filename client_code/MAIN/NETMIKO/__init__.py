from ._anvil_designer import NETMIKOTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...automation import remove_from_automation_devices_list, add_to_automation_devices_list,get_automation_devices_list, add_task_args
from anvil_extras.MultiSelectDropDown import MultiSelectDropDown
from ...globals import netmiko_device_types
from m3._Components.IconButton import IconButton
from ...tools import dict_to_paragraph
from ...bunkers import get_bunkers_list

class NETMIKO(NETMIKOTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.bunkers  = get_bunkers_list()
    self.checked_prompt = False
    self.checked_prompt_list = []
    self.netmiko_devices = []
    self.repeating_panel.items =  []
    self.init_components(**properties)
    # b = []
    # for i in range(1):
    #   a={"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None}
    #   b.append(a)
    # self.repeating_panel.items= (b)
    # Any code you write here will run before the form opens.

  def add_from_inventory_click(self, **event_args):
    """This method is called when the component is clicked."""

    # if not self.repeating_panel.items or self.repeating_panel.items == []:
    #   t = get_automation_devices_list()[:]
    #   self.repeating_panel.items = [*t]
    # else:
    self.repeating_panel.items = [*self.repeating_panel.items, *get_automation_devices_list()]

    pass


  def check_prompt_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    self.build_netmiko_list()
    if not self.netmiko_devices:
      Notification("No devices").show()
      return
    set1 = {frozenset(self.normalize_dict(d).items()) for d in self.netmiko_devices}
    set2 = {frozenset(self.normalize_dict(d).items()) for d in self.checked_prompt_list}
    if set1 == set2:
      Notification("Already Checked Prompt").show()
      return
    try:
      # r = anvil.server.call("check_prompt", self.netmiko_devices, self.bunkers_drop_menu.selected_value)
      r= {}
      r["result"] = "success"
      
      if r['result'] == "failed":
        alert(f"Checking Prompt Failed: {r}")
        return
      alert(r['result'], large=True, title="Prompt Results")
      self.checked_prompt = True
      self.checked_prompt_list = [dict(d) for d in self.netmiko_devices]
    except Exception as e:
      Notification(f"Checking Prompt had Exception: {e}").show()
      return
   

        
    


  def add_row_manually_click(self, **event_args):
    """This method is called when the component is clicked."""
    if self.repeating_panel.items:
      self.repeating_panel.items = [*self.repeating_panel.items, {"name": "zzz", "host": None,"username": None, "password": None,"port": None,"secret": None, "device_type": None}]
    else:
      self.repeating_panel.items = [{"name": "zzz", "host": None,"username": None, "password": None,"port": None,"secret": None, "device_type": None}]
    pass

  def cli_commands_text_area_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    pass

  def set_run_time_click(self, **event_args):
    """This method is called when the component is clicked."""
  
    self.build_netmiko_list()
    set1 = {frozenset(self.normalize_dict(d).items()) for d in self.netmiko_devices}
    set2 = {frozenset(self.normalize_dict(d).items()) for d in self.checked_prompt_list}

    if set1 != set2:
      self.checked_prompt = False
    if not self.checked_prompt:
      Notification("Check Prompt First").show()
      return
      
    t = {}
    t["commands"] =[line.strip() for line in self.cli_commands_text_area.text.splitlines() if line.strip()]
    t["task_friendly_name"] = self.friendly_name_text_box.text or "Netmiko_Task"
    t["devices"] = self.netmiko_devices
    # alert(f"Will Check the prompt for the following, please confirm:\n{dict_to_paragraph(t)}", large = True)
    add_task_args(t)
    f = get_open_form()
    f.sidesheet_content_col.clear()
    f.schedule_side.task_description_text_box.text = dict_to_paragraph(t)   
    f.sidesheet_content_col.add_component(f.schedule_side)
    f.layout.show_sidesheet = True
    pass
    
    
    
  def normalize_dict(self, d):
      """Convert lists in dictionary values to tuples for comparison."""
      return {k: tuple(v) if isinstance(v, list) else v for k, v in d.items()}


  def build_netmiko_list(self):
    self.netmiko_devices = []
  
    for i in self.repeating_panel.get_components():
      self.device = {}
      print('repeating_panel componenets', i.__name__)
      for r in i.get_components():
        # print('Rows componenets', r.__name__)
        if r.tag == "name":
          # print('name', r.text)
          self.device['name'] = r.text
        if r.tag == 'address':
         self. device['host'] = r.text
        if r.tag == "username":
          self.device["username"] = r.text
        if r.tag == 'password':
          self.device["password"] = r.text
        if r.tag == 'port':
          self.device["port"] = 'port'
        if r.tag == 'secret':
          self.device['secret'] = r.text
        if r.tag == 'device_type':
          self.device['device_type'] = r.selected
        if r.tag == 'is_telnet':
          # print("found telnet")
          self.device['is_telnet'] = r.checked or False
      if not self.device:
        Notification("No devices added").show()
        return
      if not all([self.device['name'],self.device['host'], self.device['username'], self.device['password'], self.device['port'], self.device['device_type'] ]):
        Notification("Name, Address, Username, Password, Port, Device Type: Are Mandatory", title="Some Fields are missing").show()
        return
      self.netmiko_devices.append(self.device)