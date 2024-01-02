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

Builder.load_file("screens/groups_view.kv")
Builder.load_file("screens/add_task.kv")


class MainApp(MDApp):
    def date_now_add_task(self, **kwargs):
        """Set current date on add task screen"""
        self.root.ids.date_text.text = str(datetime.now().strftime("%Y-%m-%d"))

    def date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_task_date)
        date_dialog.open()

    def set_task_date(self, instance, value, date_range):
        """This function gets the date from the date picker and converts in a more friendly form then changes the date label on the dialog"""
        date = value.strftime("%Y-%m-%d")
        self.root.ids.date_text.text = str(date)

    def build(self, *args):
        # Setting theme
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.material_style = "M3"


# MainApp().run()

if __name__ == "__main__":
    MainApp().run()
