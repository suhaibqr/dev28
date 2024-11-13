from ._anvil_designer import schedule_sideTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class schedule_side(schedule_sideTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.not_before = datetime.now()
    self.init_components(**properties)
    self.cols = [self.run_now_col,self.run_at_col,self,self.run_after_col,self.run_intervally_col,self.run_cron_col]
    
    # Any code you write here will run before the form opens.

  def radio_group_panel_change(self, **event_args):
    trigger_type = event_args['sender'].selected_value
    if trigger_type == 'run_now':
      for c in self.cols:
        if c.tag == trigger_type:
          c.visible =True
        else:
          c.visible = False
          


    pass

  def start_date_picker_change(self, **event_args):
    """This method is called when the selected date changes"""
    pass
