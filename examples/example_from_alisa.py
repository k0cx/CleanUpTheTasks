from kivymd.app import MDApp
from kivy.lang.builder import Builder

from kivymd.uix.screen import MDScreen

KV = """
BoxLayout:
    orientation:'vertical'

    MDBottomAppBar:
        MDTopAppBar:
            anchor_title:'left'
            anchor_bottom:'left'
            type:'bottom'
            title:'Bottom Toolbar'
            elevation:10

    FloatLayout:
        AnchorLayout:
            anchor_x:'center'
            AnchorLayout:
                anchor_x:'right'
                size_hint:(0.5,1)
                BoxLayout:
                    orientation:'vertical'
                    size_hint:(1,0.7)
                    padding:15
                    canvas.before:
                        Color:
                            rgba: 0.8,0.8,.8,1
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    Button:
                        text:'Button 1'
                        size_hint:(.5,.5)
                    Button:
                        text:"Button 2"
                        size_hint:(.5,.5)

"""


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()
