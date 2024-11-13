from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....globals import netmiko_device_types

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    self.netmiko_platforms = netmiko_device_types
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.address.text = self.item['host']
    self.device_name.text = self.item['name']
    self.username.text = self.item['username']
    self.password.text = self.item['password']
    self.port.text = self.item['port']
    self.enablesecret.text = self.item['secret']
    
    # Any code you write here will run before the form opens.

  def delete_click(self, **event_args):
    # print(type(self.parent), self.parent)
    # print(self.item)
    self.clear()
    self.parent.items.remove(self.item)
   
    # print(self.parent.items.remove())
    # row = DataRowPanel(item={"address": None,"username": None, "password": None,"port": None,"enablesecret": None, "device_type": None})
    # self.add_component(row) 
    pass
