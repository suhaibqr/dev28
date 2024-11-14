from ._anvil_designer import check_ports_taskTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from  ...bunkers import get_bunkers_list
from ...automation import add_task_args
from ...tools import  dict_to_yaml_string

class check_ports_task(check_ports_taskTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.bunkers = get_bunkers_list()
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def run_check_ports_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    hosts = self.hosts_text_area.text.strip().split(',')
    ports = self.ports_text_area.text.strip().split(',')
    if len(hosts) < 1 or len(ports) < 1:
      Notification("Make sure to Enter one of multiple IPs or Ports").show()
      return
    if not self.bunkers_list_menu.selected_value:
      Notification("Select Bunker").show()
      return
    if '' in hosts:
      hosts.remove('')
    if '' in ports:
      ports.remove('')
    body= {}
    task = {}
    task['arguments']= {}
    task['arguments']['hosts'] =hosts
    task['arguments']['ports'] = ports
    task['bunker_id'] = self.bunkers_list_menu.selected_value
    task["task_name"] = "task_check_ports"
    task["arguments"]["notify_on_error"] = True
    task["arguments"]["notify_on_success"] = True
    body["tasks"] = [task]
    
    add_task_args(body)
    f = get_open_form()
    f.sidesheet_content_col.clear()
    f.schedule_side.task_description_text_box.text = dict_to_yaml_string(body) 
    f.sidesheet_heading.text = "Set Task Timing"
    f.sidesheet_content_col.add_component(f.schedule_side)
    f.layout.show_sidesheet = True
    pass
