from ._anvil_designer import task_pingTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..bunkers import get_bunkers_list
from ..automation import add_task_args
from ..tools import dict_to_paragraph

class task_ping(task_pingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.bunkers = get_bunkers_list()
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def bunkers_drop_down_menu_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def run_ping_task_click(self, **event_args):
    """This method is called when the component is clicked."""
    ips = self.address_text_box.text.strip().split(",")
    if len(ips) < 1:
      Notification("Enter One or more IPs").show()
      return
    if '' in ips:
      ips.remove("")
    if not self.bunkers_drop_down_menu.selected_value:
      Notification("Select Bunker").show()
      return
    task = {}
    print(ips)
    task["bunker_id"] = self.bunkers_drop_down_menu.selected_value
    task["arguments"] = {}
    task["arguments"]["hosts"] = ips
    add_task_args(task)
    f = get_open_form()
    f.sidesheet_content_col.clear()
    f.schedule_side.task_description_text_box.text = dict_to_paragraph(task)   
    f.sidesheet_content_col.add_component(f.schedule_side)
    f.sidesheet_heading.text = "Set Task Timing"
    f.layout.show_sidesheet = True
    
