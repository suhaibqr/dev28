from ._anvil_designer import INVENTORYTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from ...inventory_fn import fetch_inventory_from_bunker
from ...filter import DictFilter
from ...bunkers import get_bunkers_list

class INVENTORY(INVENTORYTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_bindings()
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.


  def init_bindings(self):
    self.grid_items = []
    self.inventory_table =[]

  def get_inventory(self):
    # user = anvil.server.call("check_auth")
    # if not user:
    #   alert("Not Authenticated")
    #   return
    data = fetch_inventory_from_bunker("TDM Vertus")
    self.inventory_table = DictFilter(data,["opdevice_groupDisplayName"])

    self.inventory_rep.items = self.inventory_table.filtered_list

    
  def build_form(self):
    get_bunkers_list()
    self.get_inventory()

  def search_engine_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses enter in this component."""
    print(self.search_engine_text_box.text)
    self.inventory_table.search_by_string(self.search_engine_text_box.text)
    self.inventory_rep.items = self.inventory_table.filtered_list
   
    # self.inventory_rep.items = 
    pass
    

                                       
    