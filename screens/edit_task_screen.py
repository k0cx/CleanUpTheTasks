import platform

from datetime import datetime
from pathlib import Path

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.metrics import dp  # TODO: to be removed when dropdown items ready

from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker

from data.database import Database

# Initialize db instance
db = Database()


class CheckSwitchItem(MDBoxLayout):
    text = StringProperty()
    group = StringProperty()
    task_id = StringProperty()


class EditTaskScreen(Screen):
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
        if platform.system() == "Android":
            from android.storage import primary_external_storage_path

            primary_ext_storage = Path(primary_external_storage_path())
            self.file_manager.show(primary_external_storage_path())

        else:
            self.file_manager.show(str(Path.home()))

        self.manager_open = True

    def select_path(self, path: str):
        """
        It will be called when you click on the file name.
        :param path: path to the selected file;
        """

        self.exit_manager()
        self.ids.attachment.text = path

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device."""

        if keyboard in (1001, 27, 8):
            if self.manager_open:
                self.file_manager.back()
        return True

    def write_task(self, task, task_date):
        if self.ids.task_id.text == "":
            db.create_task(task.text, task_date)
            toast(text="added", duration=2)
        else:
            db.update_task(self.ids.task_id.text[3:], task.text, task_date)
            toast(text="updated", duration=2)

    def delete_task(self, taskid):
        # self.parent.remove_widget(the_list_item)
        db.delete_task(taskid[3:])
        # print(task_id[3:])

    def back_action(self):
        sm = MDApp.get_running_app().root
        sm.get_screen(name="task list screen").ids.bottom_nav_bar.switch_tab(
            "tasks_list"
        )
        sm.transition = SlideTransition(direction="right")
        sm.current = "task list screen"
        self.ids.task_id.text = ""
        self.ids.task_text.text = ""
        self.ids.task_description.text = ""
        self.ids.date_text.text = ""
        self.ids.attachment.text = ""
        self.ids.project.text = ""
        self.ids.context.text = ""
