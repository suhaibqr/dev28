from ._anvil_designer import my_tasksTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...filter import DictFilter

class my_tasks(my_tasksTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def search_text_box_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    
    pass

  def get_active_tasks_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    
    try:
      r = anvil.server.call("get_teams_tasks")
      if r["status"] == "failed":
        Notification("Fetching tasks Failed").show()
        return
      self.old_tasks_data_grid.visible = False
      self.team_active_tasks.visible = True
      self.active_tasks_table = DictFilter(r['results'], ['owner'])
      self.active_tasks_repeating_panel.items = self.active_tasks_table.original_list
    except Exception as e:
      Notification(f"An Error Occured while getting tasks: {e}")
    pass

  def search_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses enter in this component."""
    self.active_tasks_table.search_by_string(self.search_text_box.text)
    self.active_tasks_repeating_panel.items = self.active_tasks_table.filtered_list
    pass

  def get_old_tasks_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    try:
      r = anvil.server.call("get_old_tasks")

      if r['status'] == "failed":
        Notification("Couldnt Fetch Old data").show()
        return
      self.old_tasks_data_grid.visible = True
      self.team_active_tasks.visible = False
      self.old_tasks_table = DictFilter(r['result'])
      self.old_tasks_repeating_panel.items = self.old_tasks_table.original_list
    except Exception as e:
      Notification("Error While Getting Old Tasks").show()
      return
    pass

  def old_tasks_search_engine_box_pressed_enter(self, **event_args):
    """This method is called when the user presses enter in this component."""
    self.old_tasks_table.search_by_string(self.old_tasks_search_engine_box.text)
    self.old_tasks_repeating_panel.items = self.old_tasks_table.filtered_list
    pass
