from ._anvil_designer import automation_welcomepageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class automation_welcomepage(automation_welcomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def open_netmiko_task_form_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    f = get_open_form()
    f.main_col_panel.clear()
    f.main_col_panel.add_component(f.netmiko_task_form)
    f.layout.show_sidesheet = False
    pass
