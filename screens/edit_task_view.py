from datetime import datetime
from pathlib import Path

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker

from data.database import Database
from data.data_init import data_dir_init

cutt_data_dir = data_dir_init().dir_init()
# Initialize db instance
db = Database()


class EditTaskView(MDBoxLayout):
    def date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_task_date)
        date_dialog.open()

    def set_task_date(self, instance, value, date_range):
        """This function gets the date from the date picker
        and converts in a more friendly form
        then changes the date label on the dialog"""
        date = value.strftime("%Y-%m-%d")
        self.ids.date_text.text = str(date)

    def write_task(self, task, task_date):
        if self.ids.task_text.text == "":
            toast(text="enter task text")
        elif self.ids.task_id.text == "":
            db.create_task(task.text, task_date)
            toast(text="added", duration=3)
        else:
            db.update_task(self.ids.task_id.text[3:], task.text, task_date)
            toast(text="updated", duration=3)

    def delete_task(self, taskid):
        db.delete_task(taskid[3:])
        toast(text="deleted", duration=3)

    def clear_edit_fields(self):
        self.ids.task_id.text = ""
        self.ids.task_text.text = ""
        self.ids.date_text.text = ""
