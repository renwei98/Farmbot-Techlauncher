"""Rachel: I created this class so we can have all the sending functions in
   a nice convenient isolated class"""

from read_commands import ActionHandler
from read_CSV import MapHandler
import subscribe_to_farmbot.client as client
import subscribe_to_farmbot.my_device_id as my_device_id

def send_map(map_handler):
    """To whomever is supposed to turn CSV maps into CeleryScript
       so it can be sent to FarmBot: Please use this function so
       we can have all the sending functions in a nice convenient
       isolated class."""

def send_commands(action_handler, sequences=[], regimens=[]):
    """sequences : sequences you want to send, listed by name
       regimens  : regimens you want to send, listed by name"""
    """This function should also handle getting and updating IDs
       from sending sequences and regimens.
       It can use action_handler.update_sequence() and
                  action_handler.update_regimen()."""
