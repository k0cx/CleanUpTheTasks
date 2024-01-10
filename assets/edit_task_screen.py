import os
from datetime import datetime

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp  # TODO: to be removed when dropdown items ready

from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker

# from kivymd.uix.screen import MDScreen


from assets.database import Database

# Initialize db instance
db = Database()

# Builder.load_file("assets/add_task_screen.kv")
Builder.load_file("assets/edit_task_screen.kv")


class EditTaskScreen(Screen):
    task_text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.task_text = "text N"

    # ScreenManager().get_screen(name="edit task screen").task_text = "task_data[2]"
