from ._anvil_designer import TOOLSTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import open as open_tab
from ...bunkers import get_bunkers_list
from ...data_validation import is_valid_tcp_port
import m3.components as m3
from ...filter import transform_to_dict
was_built = False

class TOOLS(TOOLSTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def manual_ssh_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    hostname = self.address_text_box.text
    username = self.username_text_box.text
    password = self.password_text_box.text
    port = self.password_text_box.text
    bunker = self.bunkers_list.selected_value or "TDM Vertus"
    bunker = get_bunkers_list()[bunker][1]
    if not all([hostname,username,password,is_valid_tcp_port(port)]):
      alert("Make sure address, username, password and port are filled")
    url = f"{bunker}?hostname={hostname}&username={username}&password={password}&port={port}&token={token}"
    print("opening in a new tab", url)
    open_tab(url, "_blank")

  def bunkers_list_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def ping_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    if not all([self.address_text_box.text]):
      Notification("Make Sure Address field has a valid address")
    try:
      r = anvil.server.call("ping_host", self.address_text_box.text, self.port_text_box.text)
      if r["status"] == "failed":
        alert(f"Pinging Failed:\n\n {r['result']}")
      else:
        alert(r["result"])
    except Exception as e:
      alert(f"Ping failed: {e}")
    pass

  def check_port_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    if not all([self.address_text_box.text, is_valid_tcp_port(self.port_text_box.text)]):
      Notification("Make Sure Address, Port, and Bunker are selected").show()
    try:
      r = anvil.server.call("check_port", self.address_text_box.text, self.port_text_box.text)
      if r["status"] == "failed":
        alert(f"Checking Port Failed:\n\n {r['result']}")
      else:
        alert(r["result"])
    except Exception as e:
      alert(f"Ping Faild: {e}")
    pass


  def reset_form(self):
    self.documents_multi_menu.items = []


  def build_form(self):
    global was_built
    self.bunkers_list.items = list(get_bunkers_list().keys())
    self.bunkers_list.selected_value = "TDM Vertus"
    if not was_built:
      self.folder_list = anvil.server.call("get_folder_names")
    was_built = True
      
    self.documents_multi_menu.items= self.folder_list




  def documentation_dropdown_btn_menu_show(self, **event_args):
    """This method is called when the component is shown on the screen"""
    
    folder_name = event_args['sender'].selected[0]
    if folder_name == "KB Resources":
      return
    self.tree_data = anvil.server.call(
      "create_fancytree_node_tree", folder_name
    )
    # print("self.tree_data", self.tree_data)
    self.t = ColumnPanel()
    tree_dom_node = anvil.js.get_dom_node(self.t)

    # Initialize the Fancytree on the DOM node using jQuery
    anvil.js.window.jQuery(tree_dom_node).fancytree(
      {
        "checkbox": False,
        "selectMode": 1,
        "source": self.tree_data,
        "activate": lambda event, data: self.update_status_label(data.node),
      }
    )
    alert(self.t, large=True)
    pass

  def recordings_btn_click(self, **event_args):
    """This method is called when the component is clicked."""
    # try:
    bunker = self.bunkers_list.selected_value
    r = anvil.server.call("get_ssh_entries", "suhaib.alrabee@tdmgroup.net", bunker)
    r = r['result']['data']
  
    get_open_form().ssh_sessions_sidesheet(r)
    # except Exception as e:
    #   alert(f"Failed to get SSH sessions: {e}")






        
        
    