import os
from datetime import datetime

from kivy.core.window import Window
from kivy.metrics import dp  # TODO: to be removed when dropdown items ready

from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.screen import MDScreen

from database import Database


class DescriptionDialog(MDBoxLayout):
    def __init__(self, default_config=None, **kwargs):
        super().__init__(**kwargs)
        self.add_task_class = AddTask()


class AddTask(MDScreen):
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

    def project_select(self):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "text": f"Item {i}",
                "on_release": lambda x=f"Item {i}": self.project_set_item(x),
            }
            for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.project,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.open()

    def project_set_item(self, text_item):
        self.ids.project.text = text_item
        self.menu.dismiss()

    def context_select(self):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "text": f"Item {i}",
                "on_release": lambda x=f"Item {i}": self.context_set_item(x),
            }
            for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.context,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.open()

    def context_set_item(self, text_item):
        self.ids.context.text = text_item
        self.menu.dismiss()

    def file_manager_open(self):
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            selector="file",
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        """
        It will be called when you click on the file name.
        :param path: path to the selected file;
        """

        self.exit_manager()
        self.ids.attachment.text = path

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device."""

        if keyboard in (1001, 27, 8):
            if self.manager_open:
                self.file_manager.back()
        return True

    def add_task(self, task, task_date):
        """Add task to the list of tasks"""

        # TODO: use snackbar when task added
        created_task = db.create_task(task.text, task_date)
        self.root.ids["container"].add_widget(
            ListItemWithCheckbox(
                pk=created_task[0],
                text="[b]" + created_task[1] + "[/b]",
                secondary_text=created_task[2],
            )
        )

    def clear_form(self, *args):
        self.ids.task_text.text = ""
        self.ids.task_description.text = ""
        self.ids.date_text.text = ""
        self.ids.attachment.text = ""
        self.ids.project.text = ""
        self.ids.context.text = ""
