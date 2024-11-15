from ._anvil_designer import RowTemplate8Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....tools import  dict_to_yaml_string


class RowTemplate8(RowTemplate8Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def task_args_btn_click(self, **event_args):
    f =get_open_form()
    f.sidesheet_content_col.clear()
    d = {}
    d["Trigger_Details"] = self.item["kwargs"]["trigger"]
    d["Task_Arguments"] = self.item["kwargs"]["arguments"]
    d["Next_Run"] = self.item["next_run_time"]
    d["Owner"] = self.item["owner"]
    d["Task_Type"] = self.item["task_name"]
    d["Task_Friendly_name"] = self.item["user_description"]
    f.sidesheet_heading.text = "Task Details"
    t = TextArea(text=dict_to_yaml_string(d), auto_expand=True)
    f.sidesheet_content_col.add_component(t)
    f.layout.show_sidesheet = True
    
    pass

  def cancel_task_btn_click(self, **event_args):
    a = alert("Are You Sure", buttons=[("Yes", True), ("No", False)], dismissible= True)
    if a:
      print("will cancel")
      try:
        print(self.item)
        owner = "suhaib.alrabee@tdmgroup.net"
        r = anvil.server.call("cancel_active_task", [self.item['job_id']], owner)
        if r["result"] == "failed":
          Notification("Failed to Cancel job").show()
          return
        
        # self.remove_from_parent()
        # self.parent.remove(self.item)
        
        if r["status"] == "success":
          alert(f"Task was canceled\n{dict_to_yaml_string(r['result'])}")
          self.clear()
      except Exception as e:
        Notification(f"Error in Canceling job: {e}").show()




