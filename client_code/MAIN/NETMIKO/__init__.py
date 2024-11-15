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
from ...tools import  dict_to_yaml_string
from ...bunkers import get_bunkers_list
import json
import copy

class NETMIKO(NETMIKOTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.bunkers  = list(get_bunkers_list().keys())
   
    self.checked_prompt = False
    self.checked_prompt_list = []
    self.netmiko_devices = []
    self.repeating_panel.items =  []
    self.init_components(**properties)
    self.bunkers_drop_menu.selected_value = self.bunkers_drop_menu.items[0]
    # b = []
    # for i in range(1):
    #   a={"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None}
    #   b.append(a)
    # self.repeating_panel.items= (b)
    # Any code you write here will run before the form opens.

  def add_from_inventory_click(self, **event_args):
    """This method is called when the component is clicked."""

    olds = []
    for i in self.repeating_panel.get_components():
      old = {"name": i.device_name.text, "host": i.address.text, "username": i.username.text, "password": i.password.text, "port": i.port.text, "secret": i.enablesecret.text,"device_type": i.netmiko_device_type_menu.selected }
      olds.append(old)
    
    self.repeating_panel.items = [*olds, *get_automation_devices_list()]

    pass


  def check_prompt_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    a =  self.build_netmiko_list()
    if not a:
      return
  
    if not self.netmiko_devices:
      Notification("No devices").show()
      return
    set1 = {frozenset(self.normalize_dict(d).items()) for d in self.netmiko_devices}
    set2 = {frozenset(self.normalize_dict(d).items()) for d in self.checked_prompt_list}
    if set1 == set2:
      Notification("Already Checked Prompt").show()
      return

    if not self.bunkers_drop_menu.selected_value:
      Notification("Select Bunker").show()
      return
    try:
      t ={}
      t["task_name"] = "find_prompt"
      t["adhoc_args"] = {}
      t["adhoc_args"]["devices"] = self.netmiko_devices
      t["bunker_id"] = self.bunkers_drop_menu.selected_value
      t["is_config"] = self.is_config.selected
      # alert(json.dumps(t, indent =4), large=True, dismissible=True)
      r = anvil.server.call("check_prompt_task", t, self.bunkers_drop_menu.selected_value)
    
      if r['status'] == "failed":
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
    olds = []
    for i in self.repeating_panel.get_components():
      old = {"name": i.device_name.text, "host": i.address.text, "username": i.username.text, "password": i.password.text, "port": i.port.text, "secret": i.enablesecret.text,"device_type": i.netmiko_device_type_menu.selected }
      olds.append(old)

    if event_args['sender'].tag == "remove_btn":
      self.repeating_panel.items = [*olds]
      return
    
    if self.repeating_panel.items:
      self.repeating_panel.items = [*olds, {"name": "", "host": "","username": "", "password": "","port": "","secret": "", "device_type": [None]}]
    else:
      self.repeating_panel.items = [{"name": "", "host": "","username": "", "password": "","port": "","secret": "", "device_type": [None]}]
    pass

  def cli_commands_text_area_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    pass

  def set_run_time_click(self, **event_args):
    """This method is called when the component is clicked."""
  
    if not self.build_netmiko_list():
      return
    if not self.netmiko_devices:
      Notification("No Devices").show()
      return
    set1 = {frozenset(self.normalize_dict(d).items()) for d in self.netmiko_devices}
    set2 = {frozenset(self.normalize_dict(d).items()) for d in self.checked_prompt_list}

    if set1 != set2:
      self.checked_prompt = False
    if not self.checked_prompt:
      Notification("Check Prompt First").show()
      return
    if not self.bunkers_drop_menu.selected_value:
      Notification("Select Bunker").show()
      return
    body = {}
    tasks = []
    for d in self.netmiko_devices:
      print(d)
      t = {}
      t["task_name"] = "task_netmiko"
      t["arguments"] = {}
      t["arguments"]["device_name"] = d['name']
      t['arguments']["device_type"] = d['device_type'][0]
      t['arguments']['username'] = d['username']
      t['arguments']['host'] = d['host']
      t['arguments']['password'] = d['password']
      t['arguments']['port'] = d['port']
      t['arguments']['is_config'] = self.is_config.selected
      t['arguments']['use_telnet'] = d['is_telnet']
      t['arguments']['commands'] = [line.strip() for line in self.cli_commands_text_area.text.splitlines() if line.strip()]
      t['user_description'] = self.friendly_name_text_box.text
      tasks.append(t)
    body["bunker_id"] = self.bunkers_drop_menu.selected_value
    body["tasks"] = tasks
    


    
    add_task_args(copy.deepcopy(body))
    f = get_open_form()
    f.sidesheet_content_col.clear()
    # f.schedule_side.task_description_text_box.text = json.dumps(t, indent = 4)   
    f.schedule_side.task_description_text_box.text = dict_to_yaml_string(body)
    f.sidesheet_content_col.add_component(f.schedule_side)
    f.sidesheet_heading.text = "Set Task Timing"
    f.layout.show_sidesheet = True
    pass
    
    
    
  def normalize_dict(self, d):
      """Convert lists in dictionary values to tuples for comparison."""
      return {k: tuple(v) if isinstance(v, list) else v for k, v in d.items()}


  def build_netmiko_list(self):
    self.netmiko_devices = []
    if not self.repeating_panel.get_components():
      Notification("No devices added").show()
      return False
    for i in self.repeating_panel.get_components():
      if not all([i.device_name.text,i.address.text, i.username.text, i.password.text,i.port.text, i.netmiko_device_type_menu.selected ]):
        Notification("Name, Address, Username, Password, Port, Device Type: Are Mandatory", title="Some Fields are missing").show()
        return False
      row = {"name": i.device_name.text, "host": i.address.text, "username": i.username.text, "password": i.password.text, "port": i.port.text, "secret": i.enablesecret.text,"is_telnet": i.is_telnet.checked , "device_type": i.netmiko_device_type_menu.selected }
      self.netmiko_devices.append(row)
    return True

    
    # for i in self.repeating_panel.get_components():
    #   self.device = {}
    #   print('repeating_panel componenets', i.__name__)
    #   for r in i.get_components():
    #     # print('Rows componenets', r.__name__)
    #     if r.tag == "name":
    #       # print('name', r.text)
    #       self.device['name'] = r.text
    #     if r.tag == 'address':
    #      self. device['host'] = r.text
    #     if r.tag == "username":
    #       self.device["username"] = r.text
    #     if r.tag == 'password':
    #       self.device["password"] = r.text
    #     if r.tag == 'port':
    #       self.device["port"] = 'port'
    #     if r.tag == 'secret':
    #       self.device['secret'] = r.text
    #     if r.tag == 'device_type':
    #       self.device['device_type'] = r.selected
    #     if r.tag == 'is_telnet':
    #       # print("found telnet")
    #       self.device['is_telnet'] = r.checked or False
    #   if not self.device:
    #     # Notification("No devices added").show()
    #     return
    #   if not all([self.device['name'],self.device['host'], self.device['username'], self.device['password'], self.device['port'], self.device['device_type'] ]):
    #     Notification("Name, Address, Username, Password, Port, Device Type: Are Mandatory", title="Some Fields are missing").show()
    #     return False
    #   self.netmiko_devices.append(self.device)
    #   return True