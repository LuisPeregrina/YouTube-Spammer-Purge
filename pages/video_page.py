from tkinter.constants import BOTH, BOTTOM, E, LEFT, RIGHT, TOP, W, X, Y, YES
from . import *

class VideoPage(Page):
    title = "Search single video"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.parent_frame = Frame(self)
        self.parent_frame.columnconfigure(1, weight=1)
        self.parent_frame.rowconfigure(1, weight=1)
        label = Label(self.parent_frame, text="Select the :")
        label.grid(column=0, row=0)
        video_id = Entry(self.parent_frame)
        video_id.grid(column=1, row=0)
        button = Button(self.parent_frame, text='Continue', command=self.continue_search)
        button.grid(column=0, row=1, columnspan=2, sticky=E+W)
        self.parent_frame.pack()

    def continue_search(self):
        self.controller.ask(message="Are you sure about that?")
        self.parent_frame.pack_forget()
        self.parent_frame.destroy()

        self.parent_frame = Frame(self)
        label = Label(self.parent_frame, text="Enter Video link or ID to scan:")
        label.pack(side=LEFT)
        video_id = Entry(self.parent_frame)
        video_id.pack(side=RIGHT)
        button = Button(self.parent_frame, 'Continue', command=self.continue_search)
        button.pack(side=BOTTOM)
        self.parent_frame.pack(pady=1, padx=1)
