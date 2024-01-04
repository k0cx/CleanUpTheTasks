from kivy.config import Config

Config.set("graphics", "resizable", True)
Config.set("graphics", "width", "350")
Config.set("graphics", "height", "600")
Config.set("kivy", "exit_on_escape", "0")

from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

# from kivymd.uix.dialog import MDDialog
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.pickers import MDDatePicker
# from kivymd.uix.button import MDFlatButton

# from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
# from kivymd.uix.selectioncontrol import MDCheckbox
# from kivymd.uix.toolbar.toolbar import MDFabBottomAppBarButton
# from kivymd.uix.toolbar import MDTopAppBar

from datetime import datetime

from screens.add_task import AddTask, DescriptionDialog

Builder.load_file("screens/groups_view.kv")
Builder.load_file("screens/add_task.kv")


class MainApp(MDApp):
    def build(self, *args):
        # Setting theme
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.material_style = "M3"


# MainApp().run()

if __name__ == "__main__":
    MainApp().run()
