from ._anvil_designer import RowTemplate9Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....tools import dict_to_yaml_string


class RowTemplate9(RowTemplate9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def old_task_args_btn_click(self, **event_args):
    f =get_open_form()
    f.sidesheet_content_col.clear()
    d = {}
    d["Trigger_Details"] = self.item["trigger"]
    d["Tassk_Arguments"] = self.item["arguments"]
    d["Owner"] = self.item["owner"]
    d["Task_Type"] = self.item["task_type"]
    d["Task_Friendly_name"] = self.item["task_friendly_name"]
    d["Started_At"] = self.item["started_at"]
    d["Finished_At"] = self.item["finished_at"]
    
    f.sidesheet_heading.text = "Task Details"
    t = TextArea(text=dict_to_yaml_string(d))
    
    f.sidesheet_content_col.add_component(t)
    f.layout.show_sidesheet = True
    pass

  def download_result_btn_click(self, **event_args):
    try:
      r = anvil.server.call("get_old_task_details", self.item['user_job_id'])
      anvil.BlobMedia('text/plain', r['result'])
      if r['status'] == "failed":
        Notification("Couldnt Fetch Old Task details").show()
        return
      alert(r['result'], large=True)
    except Exception as e:
      Notification("Error while getting Task Results").show()
      return
    pass


  def check_old_task_args_btn_click(self, **event_args):
    f = get_open_form()
    f.sidesheet_heading.text = "Task Details"
    # print("self.item['arguments']", type(self.item['arguments']), self.item['arguments'])
    t = TextArea(text=dict_to_yaml_string(dict_to_yaml_string(self.item['arguments'])), auto_expand=True)
    f.sidesheet_content_col.clear()
    f.sidesheet_content_col.add_component(t)
    f.layout.show_sidesheet = True
    pass

  def view_result_btn_click(self, **event_args):
    # try:
      r = anvil.server.call("get_task_result", self.item['user_job_id'])
      if r['status'] != "success":
        Notification(f"Failed to get result: {r['result']}").show()
      # alert(r['result'], large=True, dismissible=True)
      f = get_open_form()
      print(r['result'])
      f.user_task_jobs_side.repeating_panel.items = r['result']
      f.sidesheet_content_col.clear()
      f.sidesheet_content_col.add_component(f.user_task_jobs_side)
      f.layout.show_sidesheet = True
    #   return
    # except Exception as e:
    #   Notification(f"Error in getting result: {e}")



