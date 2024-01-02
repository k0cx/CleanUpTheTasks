# from kivy.config import Config

# Config.set("graphics", "resizable", True)
# Config.set("graphics", "width", "350")
# Config.set("graphics", "height", "600")

from kivy.lang import Builder

# from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker

# from kivymd.uix.button import MDFlatButton

# from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
# from kivymd.uix.selectioncontrol import MDCheckbox
# from kivymd.uix.toolbar.toolbar import MDFabBottomAppBarButton
# from kivymd.uix.toolbar import MDTopAppBar

from datetime import datetime

# with open("add_task.kv", encoding="utf-8") as KV:
#     Builder.load_string(KV.read())

# Builder.load_file("add_task.kv")


class AddTask(MDScreen):
    def date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_task_date)
        date_dialog.open()

    def set_task_date(self, instance, value, date_range):
        """This function gets the date from the date picker and converts in a more friendly form then changes the date label on the dialog"""
        date = value.strftime("%Y-%m-%d")
        self.ids.date_text.text = str(date)

    # def add_task(self, task, task_date):
    #     """Add task to the list of tasks"""

    #     created_task = db.create_task(task.text, task_date)
    #     self.root.ids["container"].add_widget(
    #         ListItemWithCheckbox(
    #             pk=created_task[0],
    #             text="[b]" + created_task[1] + "[/b]",
    #             secondary_text=created_task[2],
    #         )
    #     )

    def clear_form(self):
        self.ids.task_text.text = ""
        self.ids.task_description.text = ""
        self.ids.date_text.text = "-"
        self.ids.attachment.text = "attach file:"
