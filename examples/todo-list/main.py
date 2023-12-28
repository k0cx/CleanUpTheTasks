"""
https://dev.to/ngonidzashe/how-to-create-a-simple-to-do-list-application-with-kivymd-d89

https://github.com/Ngonie-x/todo-application-kivymd

Packaging for android
I have included all the code on github, including the spec file I used to generate the apk.

A few changes are required so that we can create an android application. Edit main.py as follows:
#...
from kivymd.uix.pickers import MDDatePicker # Here, instead of kivymd,uix.picker

# add the following just under the imports
if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

The above code will prompt the user to allow the application to access storage.

Main changes in the buildozer spec file are as follows:
requirements = python3, kivy==2.1.0, https://github.com/kivymd/KivyMD/archive/master.zip,sdl2_ttf==2.0.15,pillow,android

And
android.permissions = WRITE_EXTERNAL_STORAGE
"""

# main.py
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

from database import Database

# Initialize db instance
db = Database()


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    """Custom list item"""

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def mark(self, check, the_list_item):
        """mark the task as complete or incomplete"""
        if check.active == True:
            # add strikethrough to the text if the checkbox is active
            the_list_item.text = "[s]" + the_list_item.text + "[/s]"
            db.mark_task_as_complete(the_list_item.pk)  # here
        else:
            the_list_item.text = str(
                db.mark_task_as_incomplete(the_list_item.pk)
            )  # here

    def delete_item(self, the_list_item):
        """Delete the task"""
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom left container"""


class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the date_text label to today's date when user first opens dialog box
        self.ids.date_text.text = str(datetime.now().strftime("%A %d %B %Y"))

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)


class MainApp(MDApp):
    task_list_dialog = None  # Here

    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "DeepPurple"

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        """Add task to the list of tasks"""

        created_task = db.create_task(task.text, task_date)
        self.root.ids["container"].add_widget(
            ListItemWithCheckbox(
                pk=created_task[0],
                text="[b]" + created_task[1] + "[/b]",
                secondary_text=created_task[2],
            )
        )

        # set the dialog entry to an empty string(clear the text entry)
        task.text = ""

    def on_start(self):
        """Load the saved tasks and add them to the MDList widget when the application starts"""
        try:
            completed_tasks, uncomplete_tasks = db.get_tasks()

            if uncomplete_tasks != []:
                for task in uncomplete_tasks:
                    add_task = ListItemWithCheckbox(
                        pk=task[0], text=task[1], secondary_text=task[2]
                    )
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(
                        pk=task[0],
                        text="[s]" + task[1] + "[/s]",
                        secondary_text=task[2],
                    )
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    app = MainApp()
    app.run()
