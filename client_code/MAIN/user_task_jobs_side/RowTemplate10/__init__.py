from ._anvil_designer import RowTemplate10Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate10(RowTemplate10Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def view_job_btn_click(self, **event_args):
    t = TextArea(text=self.item['result'], auto_expand=True)
    alert(t, large=True, dismissible=True)

  def download_job_btn_click(self, **event_args):
    m = anvil.BlobMedia('text/plain', str(self.item['result']).encode(), name=f'{self.item["task_name"]}_{self.item["started_at"]}.txt')
    anvil.download(m)
    pass
    
