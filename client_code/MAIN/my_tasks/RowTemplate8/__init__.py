from ._anvil_designer import RowTemplate8Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....tools import dict_to_paragraph

class RowTemplate8(RowTemplate8Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def task_args_btn_click(self, **event_args):
    f =get_open_form()
    f.sidesheet_content_col.clear()
    d = {}
    d["Trigger_Details"] = self.item["trigger"]
    d["Tassk_Arguments"] = self.item["arguments"]
    d["Next_Run"] = self.item["next_run"]
    d["Owner"] = self.item["owner"]
    d["Task_Type"] = self.item["task_type"]
    d["Task_Friendly_name"] = self.item["task_friendly_name"]
    f.side_sheet_heading.text = "Task Details"
    t = TextArea(text=dict_to_paragraph(d))
    f.sidesheet_content_col.add_component(t)
    f.layout.show_sidesheet = True
    
    pass

  def cancel_task_btn_click(self, **event_args):
    a = alert("Are You Sure", buttons=[("Yes", True), ("No", False)], dismissible= True)
    if a:
      print("will cancel")
    else:
      print("will not cancel")
    
    pass

