from kivy.lang import Builder

from kivymd.app import MDApp

KV = """
BoxLayout:
    orientation: "vertical"

    MDLabel:
        text: "Content"
        halign: "center"

    MDBottomAppBar:

        MDTopAppBar:
            title: "MDToolbar"
            type: "bottom"
            left_action_items: [["filter"]]
            right_action_items: [["filter"]]
"""


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()
