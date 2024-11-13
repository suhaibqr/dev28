import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert, get_open_form
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

task_args = {}


t = []
t1 = {"name":"n1", "host": "a1","username": "i1", "password": "p1","port": "po1","secret": "pe1", "device_type": ["cisco_ios"]}
# t2 = {"name": "n2", "host": "a2","username": "u2", "password": "p2","port": "po2","secret": "pe2", "device_type": "plat2"}

t.append(t1)
# t.append(t2)

automation_devices_list =t

def get_automation_devices_list():
  # print("automation_devices_list", automation_devices_list)
  return automation_devices_list
  
def add_to_automation_devices_list(d):
  global automation_devices_list
  if check_if_inside_automation_list(d):
    alert("Device Already Added")
  automation_devices_list.append(d)
  get_open_form().automation_navigation_link.badge_count  += 1
  print("automation_list_after_adding", automation_devices_list)
  return automation_devices_list

def remove_from_automation_devices_list(d):
  global automation_devices_list
  new = automation_devices_list[:]
  for i in automation_devices_list:
    if d["hostname"] == i["hostname"] and d["username"] == i["username"]:
      new.remove(i)
      get_open_form().automation_navigation_link.badge_count  -= 1
  automation_devices_list = new
  print("automation_list_after_deletion", automation_devices_list)

def check_if_inside_automation_list(d):
    for i in automation_devices_list:
      if d["hostname"] == i["hostname"] and d["username"] == i["username"]:
        return True
    return False

def add_task_args(t):
  global pending_task
  pending_task = t


def get_task_args():
  return pending_task

  
  