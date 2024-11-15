from ._anvil_designer import my_tasksTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...filter import DictFilter_2 , DictFilter_3
from ...tools import dict_to_yaml_string

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
    print("get active tasks")
    try:
      r = anvil.server.call("get_active_tasks", self.is_all_switch.selected)
      print("r", r)
      if r["status"] == "failed":
        Notification("Fetching tasks Failed").show()
        return
      if r['detail'] == 'No scheduled tasks found.':
        Notification("No Active Tasks").show()
        return
      self.old_tasks_data_grid.visible = False
      self.team_active_tasks.visible = True
      
      
      self.active_tasks_table = DictFilter_2(r['result'], ['owner'])
      # print("self.active_tasks_table.original_list", self.active_tasks_table.original_list)
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
      r = anvil.server.call("get_old_tasks", self.is_all_switch.selected)
      if r['status'] == "failed":
        Notification("Couldnt Fetch Old data").show()
        return
      self.old_tasks_data_grid.visible = True
      self.team_active_tasks.visible = False
      self.old_tasks_table = DictFilter_3(self.flatten_tasks_with_keys(r['result']), ["task_name"])
      # print("self.old_tasks_table.original_list",self.old_tasks_table.original_list )
      self.old_tasks_repeating_panel.items = self.old_tasks_table.original_list
    except Exception as e:
      Notification(f"Error While Getting Old Tasks: {e}").show()
      return
    pass

  def old_tasks_search_engine_box_pressed_enter(self, **event_args):
    """This method is called when the user presses enter in this component."""
    # print("searching")
    self.old_tasks_table.search_by_string(self.old_tasks_search_engine_box.text)
    self.old_tasks_repeating_panel.items = self.old_tasks_table.filtered_list
    pass

  def is_all_switch_change(self, **event_args):
    """This method is called when the state of the component is changed."""
    pass




  def flatten_tasks_with_keys(self, task_list):
      """
      Flatten a nested list of task dictionaries into a single list of tasks, 
      including the parent key within each task.
  
      Args:
          task_list (list): List of dictionaries with tasks.
  
      Returns:
          list: A flattened list of task dictionaries with parent keys included.
      """
      flattened_list = []
      
      for task_dict in task_list:
          for key, tasks in task_dict.items():
              for task in tasks:
                  task_with_key = task.copy()
                  task_with_key['user_job_id'] = key
                  flattened_list.append(task_with_key)
      
      return flattened_list

  def cancel_all_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    a = alert("Are You Sure", buttons=[("Yes", True), ("No", False)], dismissible= True)
    if a:
      print("will cancel")
      try:
        # print(self.item)
        owner = "suhaib.alrabee@tdmgroup.net"
        r = anvil.server.call("cancel_active_task", "all", owner)
        if r["result"] == "failed":
          Notification("Failed to Cancel job").show()
          return  
        # self.remove_from_parent()
        # self.parent.remove(self.item)
        
        if r["status"] == "success":
          alert(f"Task was canceled\n{dict_to_yaml_string(r['result'])}")
          self.active_tasks_repeating_panel.items = []
      except Exception as e:
        Notification(f"Error in Canceling job: {e}").show()

    pass
