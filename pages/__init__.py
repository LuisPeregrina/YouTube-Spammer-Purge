from tkinter.constants import LEFT, TOP, X
from tkinter.ttk import *


class Page(Frame):
    title = "Page"

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        top_frame = Frame(self)
        if str(self).split('.!')[-1] != controller.PAGES[0].__name__.lower():
            Button(
                top_frame,
                text="<",
                command=lambda: controller.show_first_frame(),
                width=3
            ).pack(side=LEFT, padx=5)
        Label(
            top_frame,
            text=self.title,
            font=controller.title_font
        ).pack(side=LEFT, fill=X)
        top_frame.pack(side=TOP, fill=X)
