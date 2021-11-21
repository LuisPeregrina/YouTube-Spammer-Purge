from tkinter import Listbox, StringVar
from tkinter import W, E
from . import *

class ChannelPage(Page):
    title = "Search complete channel"
    selected_channel = None
    channels_map = [{'id':'fakeid', 'title':'Please click refresh'}]

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.parent_frame = Frame(self)
        self.parent_frame.columnconfigure(1, weight=1)
        self.parent_frame.rowconfigure(1, weight=1)
        label = Label(self.parent_frame, text="Select the channel:")
        label.grid(column=0, row=0)

        channel_list_values = StringVar(value=[c['title'] for c in self.channels_map])
        channel_listbox = Listbox(self.parent_frame, listvariable=channel_list_values )
        channel_listbox.grid(column=1, row=0)
        channel_listbox.bind('<<ListboxSelect>>', self.set_channel_selected)
        
        
        refresh_button= Button(self.parent_frame, text="↻ Refresh", command=self.refresh_channel_list)
        refresh_button.grid(column=0, row=2)

        button = Button(self.parent_frame, text='Continue', command=self.continue_search)
        button.grid(column=1, row=2, sticky=E+W)
        self.parent_frame.pack()

    def refresh_channel_list(self):
        channels_map = self.controller.fetch_channels()

    def continue_search(self):
        self.controller.show_info(message=f"Selected value was {self.selected_channel['title']} ({self.selected_channel['id']})")

    def set_channel_selected(self, event):
        widget = event.widget
        try:
            selection = widget.curselection()
            print('\nselection = ', selection)
            selection_index = int(selection[0])
            print('selection_index = ', selection_index)
            selected_channel_name = widget.get(selection[0])
            self.selected_channel = next(filter(lambda channel: channel['title'] == selected_channel_name, self.channels_map))
        except:
            raise
