from . import *

class StartPage(Page):
    title = "This is the first page"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        button1 = Button(self, text="Search video",
                         command=lambda: controller.show_frame('VideoPage'))
        button2 = Button(self, text="Search channel",
                         command=lambda: controller.show_frame('ChannelPage'))
        button1.pack()
        button2.pack()
