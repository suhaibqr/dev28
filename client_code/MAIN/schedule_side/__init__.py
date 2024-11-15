from ._anvil_designer import schedule_sideTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime , timedelta
from ...tools import dict_to_yaml_string
# from ...bunkers import get_bunkers_list
from ...automation import get_task_args
from ...globals import get_team_emails
import json

class schedule_side(schedule_sideTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
   
    self.not_before = datetime.now()
    self.team_emails = get_team_emails()
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
      task["run_at"] = str(self.run_at_date_picker.date)
    if trig == "interval":
      task['trigger'] = "interval"
     
      if not self.interval_min_box.text or not self.interval_min_box.text.isdigit():
        Notification("Enter valid interval").show()
        return
      task['interval_minutes'] = self.interval_min_box.text
      if not self.start_date_picker.date and not self.start_from_switch.selected:
        Notification("Start date is mandatory").show()
        return
      if not self.start_from_switch.selected:
        task["start_date"] = str(self.start_date_picker.date)
      if not self.end_date_switch.selected:
        if not self.end_date_picker.date:
          Notification("End Date is Mandatory").show()
          return
        task["end_date"] = str(self.end_date_picker.date)
      else:
        if not self.end_date_text_box.text or not self.end_date_text_box.text.isdigit():
          Notification("Period is Mandatory").show()
          return
        task["end_date"]  = str(datetime.now() + timedelta(minutes=int(self.end_date_text_box.text)))

    if trig == "cron":
      task['trigger'] = "cron"
      if not self.cron_text_box.text:
        Notification("Cron tab is mandatory").show()
        return
      task["cron"] = self.cron_text_box.text

    recipients = self.emails_text_area.text.split(";") or None
    if "" in recipients:
      recipients.remove("")

    # if not self.bunkers_list_menu.selected_value:
    #   Notification("Please Select Bunker")
    if not self.radio_group_panel.selected_value:
      Notification("You have to select trigger type").show()
      return
    # print("get_task_args",get_task_args())
    body =  get_task_args()
    print("body", body)
    if not input:
      Notification("No Task to add").show()
      return
    
    for b in body['tasks']:
      b["notification_details"] = {}
      b["notification_details"]["channels"] = ["email"]
      b["notification_details"]["recipients"] = recipients
      # b['user_description'] = 
      b.update(**task)

    

    self.result.content = json.dumps(body, indent = 4)
    try:
      r = anvil.server.call("schedule_task", body, "TDM")
      alert(dict_to_yaml_string(r["result"]), large=True, dismissible=True)
      
    except Exception as e:
      Notification(f"An Error Occured: {e}")
    # pass

  def task_description_text_box_show(self, **event_args):
    """This method is called when the component is shown on the screen."""
    pass

  def team_emails_menu_change(self, **event_args):
    """This method is called when the selected values change"""
    for i in self.team_emails_menu.items:
      if i['value'] in self.emails_text_area.text and i['value'] in self.team_emails_menu.selected:
        pass
      if i['value'] in self.emails_text_area.text and i['value'] not in self.team_emails_menu.selected:
        print(i['value'], "removing")
        self.emails_text_area.text = self.emails_text_area.text.replace(i['value'], "").strip()
        self.emails_text_area.text = self.emails_text_area.text.replace(f";{i['value']}", "").strip()
      if i['value'] not in self.emails_text_area.text and i['value'] in self.team_emails_menu.selected:
        self.emails_text_area.text = f"{self.emails_text_area.text};{i['value']}"
      if self.emails_text_area.text == ";":
        self.emails_text_area.text = ""
    self.emails_text_area.text = self.emails_text_area.text.replace(";;", ";").strip()
    if not self.emails_text_area.text or self.emails_text_area.text == ";" or self.emails_text_area.text == "":
      self.emails_text_area.text = ';'.join(self.team_emails_menu.selected)
      
    

   
