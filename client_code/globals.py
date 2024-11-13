import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
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
  



netmiko_device_types = [
    "a10",
    "accedian",
    "alcatel_aos",
    "arista_eos",
    "aruba_os",
    "aruba_osswitch",
    "avaya_ers",
    "avaya_vsp",
    "brocade_fastiron",
    "brocade_netiron",
    "brocade_vdx",
    "brocade_vyos",
    "checkpoint_gaia",
    "ciena_saos",
    "cisco_asa",
    "cisco_ios",
    "cisco_nxos",
    "cisco_s300",
    "cisco_tp",
    "cisco_wlc",
    "cisco_xe",
    "cisco_xr",
    "dell_dnos6",
    "dell_dnos9",
    "dell_force10",
    "eltex",
    "enterasys",
    "extreme_ers",
    "extreme_exos",
    "extreme_netiron",
    "extreme_nos",
    "extreme_slx",
    "extreme_vdx",
    "extreme_vsp",
    "extreme_wing",
    "f5_ltm",
    "fortinet",
    "generic",
    "hp_comware",
    "hp_procurve",
    "huawei",
    "juniper",
    "juniper_junos",
    "linux",
    "mellanox",
    "mikrotik",
    "mrv_optiswitch",
    "netapp_cdot",
    "netscaler",
    "oneaccess_oneos",
    "ovs_linux",
    "paloalto_panos",
    "pluribus",
    "quanta_mesh",
    "rad_etx",
    "ruckus_fastiron",
    "ubiquiti_edge",
    "ubiquiti_edgeswitch",
    "ubiquiti_unifi",
    "vyatta_vyos",
    "vyos",
]