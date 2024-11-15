from ._anvil_designer import MAINTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from .INVENTORY import INVENTORY
from .DEVICE_DETAILS_SIDE import DEVICE_DETAILS_SIDE
from .TOOLS import TOOLS
from .SSH_SESSION import SSH_SESSION
from ..bunkers import get_bunkers_list
from .schedule_side import schedule_side
from .automation_welcomepage import automation_welcomepage
from .NETMIKO import NETMIKO
from .check_ports_task import check_ports_task
from ..task_ping import task_ping
from .my_tasks import my_tasks
from .user_task_jobs_side import user_task_jobs_side
was_built = []

class MAIN(MAINTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.username_welcome_message = "Please Login To Use All Tools"
    self.init_components(**properties)
    if anvil.users.get_user():
      print(f"logged in: {anvil.users.get_user()}")
      print("icon type", type(self.login_nav.icon))
      self.login_nav.icon = "mi:logout"
      self.login_nav.text = "Log Out"
      self.is_auth = anvil.users.get_user()
      self.username_welcome_message.text = f"Welcome {anvil.users.get_user()}"
    else:
      print("No Auth")
      self.login_nav.icon = "mi:login"
      self.login_nav.text = "Log in"
      self.is_auth = None
    self.init_forms()
    print(self.login_nav.icon)
    self.layout.show_sidesheet = False
    # Any code you write here will run before the form opens.

  
  def show_device_details(self, data):
    self.sidesheet_content_col.clear()
    self.device_details_form.reset_form()
    self.device_details_form.rebuild_form()
    self.sidesheet_content_col.add_component(self.device_details_form)
 
    self.layout.show_sidesheet()
    pass

  def init_forms(self):
    self.inventory_form = INVENTORY()
    self.device_details_form = DEVICE_DETAILS_SIDE()
    self.ssh_sessions_form = SSH_SESSION()
    self.schedule_side = schedule_side()
    self.netmiko_task_form = NETMIKO()
    self.automation_welcome = automation_welcomepage()
    self.automation_navigation_link.badge = True
    self.automation_navigation_link.badge_count = 0
    self.tools_form = TOOLS()
    self.ping_task_form = task_ping()
    self.my_tasks_form = my_tasks()
    self.user_task_jobs_side = user_task_jobs_side()
    self.check_ports_task_form = check_ports_task()
    pass

  def inventory_nav_btn_click(self, **event_args):
    if "inventory_form" not in was_built:
      self.inventory_form.build_form()
      was_built.append("inventory_form")
    self.inventory_form.remove_from_parent()
    self.main_col_panel.clear()
    if self.main_col_panel.get_components():
      return
    self.main_col_panel.add_component(self.inventory_form)
    """This method is called when the component is clicked"""
    pass

  def device_details_sidesheet(self, data):
    self.sidesheet_content_col.clear()
    self.device_details_form.remove_from_parent()
    self.device_details_form.reset_form()
    self.device_details_form.rebuild_form(data)
    self.sidesheet_content_col.add_component(self.device_details_form)
    self.layout.show_sidesheet = True
    # print(dir())

  def sidesheet_icon_button_click(self, **event_args):
    self.layout.show_sidesheet = False
    pass

  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""

    pass

  def tools_navigation_link_click(self, **event_args):
    """This method is called when the component is clicked"""
    self.sidesheet_content_col.clear()
    self.main_col_panel.clear()
    self.tools_form.remove_from_parent()
    self.tools_form.reset_form()
    self.tools_form.build_form()
    if self.main_col_panel.get_components():
      return
    self.main_col_panel.add_component(self.tools_form)
    
    
  def ssh_sessions_sidesheet(self, d):
    self.sidesheet_content_col.clear()
    self.ssh_sessions_form.remove_from_parent()
    self.ssh_sessions_form.reset_form()
    self.ssh_sessions_form.build_form(d)
    self.sidesheet_content_col.add_component(self.ssh_sessions_form)
    self.layout.show_sidesheet = True

  def automation_navigation_link_click(self, **event_args):
    """This method is called when the component is clicked"""
    self.main_col_panel.clear()
    self.main_col_panel.add_component(self.automation_welcome)
    pass

  def my_tasks_nav_btn_click(self, **event_args):
    """This method is called when the component is clicked"""
    self.main_col_panel.clear()
    self.main_col_panel.add_component(self.my_tasks_form)
    pass

  def login_nav_click(self, **event_args):
    """This method is called when the component is clicked"""
    anvil.js.window.open("https://devtest.tdmgroup.net:8000/auth/saml/login", "_self")
    pass
