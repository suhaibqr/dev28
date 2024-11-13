from ._anvil_designer import RowTemplate9Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ....tools import dict_to_paragraph


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
    
    f.side_sheet_heading.text = "Task Details"
    t = TextArea(text=dict_to_paragraph(d))
    f.sidesheet_content_col.add_component(t)
    f.layout.show_sidesheet = True
    pass

  def old_task_result_btn_click(self, **event_args):
    try:
      r = anvil.server.call("get_old_task_details", self.item['task_id'])
      if r['status'] == "failed":
        Notification("Couldnt Fetch Old Task details").show()
        return
      alert(r['result'], large=True)
    except Exception as e:
      Notification("Error while getting Task Results").show()
      return
    pass
