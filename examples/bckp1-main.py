from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDFlatButton

# from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
# from kivymd.uix.selectioncontrol import MDCheckbox
# from kivymd.uix.toolbar.toolbar import MDFabBottomAppBarButton
# from kivymd.uix.toolbar import MDTopAppBar

from datetime import datetime

# with open("main.kv", encoding="utf-8") as KV:
#     Builder.load_string(KV.read())


class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the date_text label to today's date when user first opens dialog box
        self.ids.date_text.text = str(datetime.now().strftime("%Y-%m-%d"))

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = value.strftime("%Y-%m-%d")
        self.ids.date_text.text = str(date)


class MainApp(MDApp):
    task_list_dialog = None

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
                buttons=[
                    MDFlatButton(text="[b]SAVE[/b]", on_release=self.close_dialog),
                    MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                ],
            )
        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def build(self, *args):
        # Setting theme
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.material_style = "M2"


MainApp().run()

# if __name__ == "__main__":
#     app = MainApp()
#     app.run()
