from ._anvil_designer import schedule_sideTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime , timedelta
from ...tools import dict_to_paragraph
# from ...bunkers import get_bunkers_list
from ...automation import get_task_args


class schedule_side(schedule_sideTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
   
    self.not_before = datetime.now()
    # self.bunkers = get_bunkers_list()
    self.init_components(**properties)
    self.cols = [self.run_now_col,self.run_at_col,self.run_after_col,self.run_intervally_col,self.run_cron_col]
    
    # Any code you write here will run before the form opens.

  def radio_group_panel_change(self, **event_args):
    trigger_type = event_args['sender'].selected_value
    # print("trigger_type", trigger_type)
  
    for c in self.cols:
      # print("tag:", str(c.tag), "trigger_type:", trigger_type )
      if str(c.tag) in str(trigger_type):
        # print("vv")
        c.visible =True
      else:
        # print("xx")
        c.visible = False
          


    pass

  def start_date_picker_change(self, **event_args):
    """This method is called when the selected date changes"""
    pass

  def start_from_switch_change(self, **event_args):
    """This method is called when the state of the component is changed."""
    if event_args['sender'].selected:
      self.start_date_picker.enabled = False
    else:
      self.start_date_picker.enabled = True

  def end_date_switch_change(self, **event_args):
    """This method is called when the state of the component is changed."""
    if event_args['sender'].selected:
      self.end_date_picker.enabled = False
      self.end_date_text_box.enabled = True
    else:
      self.end_date_picker.enabled = True
      self.end_date_text_box = False
    pass

  def run_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    trig = self.radio_group_panel.selected_value
    # print("trigger", type(trig) , type("run_"))
    
    # print("run_after" == trig)
   
    task = {}
    if trig == "run_now":
      task["trigger"] = trig
    if trig == "run_after":
      task['trigger'] = "run_after"
      if not self.run_after_min_box.text or not self.run_after_min_box.text.isdigit():
        Notification("Make sure you have enteres a number in the minuits field").show()
        return
      else:
        task['run_after'] = self.run_after_min_box.text
    if trig == "run_at":
      if not self.run_at_date_picker.date:
        Notification("Select Date").show()
        return
      task["trigger"] = "run_at"
      task["run_at"] = self.run_at_date_picker.date
    if trig == "interval":
      task['trigger'] = "ïnterval"
     
      if not self.interval_min_box.text or not self.interval_min_box.text.isdigit():
        Notification("Enter valid interval").show()
        return
      task['min'] = self.interval_min_box.text
      if not self.start_date_picker.date and not self.start_from_switch.selected:
        Notification("Start date is mandatory").show()
        return
      if not self.start_from_switch.selected:
        task["start_date"] = self.start_date_picker.date
      if not self.end_date_switch.selected:
        if not self.end_date_picker.date:
          Notification("End Date is Mandatory").show()
          return
        task["end_date"] = self.end_date_picker.date
      else:
        if not self.end_date_text_box.text or not self.end_date_text_box.text.isdigit():
          Notification("Period is Mandatory").show()
          return
        task["end_date"]  = datetime.now() + timedelta(minutes=int(self.end_date_text_box.text))

    if trig == "cron":
      task['trigger'] = "cron"
      if not self.cron_text_box.text:
        Notification("Cron tab is mandatory").show()
        return
      task["cron_tab"] = self.cron_text_box.text

    task["recipient"] = self.emails_text_area.text.split(";") or None

    # if not self.bunkers_list_menu.selected_value:
    #   Notification("Please Select Bunker")
    if not self.radio_group_panel.selected_value:
      Notification("You have to select trigger type").show()
      return
    # print("get_task_args",get_task_args())
    if not get_task_args():
      Notification("No Task to add").show()
      return
    task.update({"arguments": get_task_args()})
    task.update({"notifications": ["email"]})
    self.result.content = dict_to_paragraph(task)
    print(task)
      # task['start_date'] = self.start_date_picker.date or 
    pass
   
