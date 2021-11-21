from . import *

class HelpPage(Page):
    title= 'Help'

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        text = Label(self, text="""
        a
        b
        c
        """
        )

        text.pack(side='left')
