import anvil.server
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

side_panel_data = []

def say_hello():
  print("Hello, world")


def set_side_panel_data(d):
  global side_panel_data
  side_panel_data =[]
  side_panel_data.append(d)

def get_side_panel_data():
  return side_panel_data.pop()
  
  