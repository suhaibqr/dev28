from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.

    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def ssh_session_link_click(self, **event_args):
    """This method is called clicked"""
    print("filename", event_args["sender"].item['filename'])
    m = anvil.server.call('get_ssh_file', event_args["sender"].item['filename'])
    print(m)
    if m:
      anvil.media.download(m)
    pass
