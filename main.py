from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")

from kivymd.app import MDApp

from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime

from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
