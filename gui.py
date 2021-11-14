from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
from tkinter import font as tkfont
import os
from datetime import datetime
import traceback
import re

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from constants import *

PAGES = [
    'StartPage',
    'SingleVideoPage',
    'CompleteChannelPage',
    'PageHelp'
]

# Default values for global variables
spamCommentsID = []
vidIdDict = {}
scannedRepliesCount = 0
scannedCommentsCount = 0
regexPattern = ''

# Declare Default Variables
maxScanNumber = 999999999
deletionEnabled = 'False' # Disables deletion functionality, which is default until later - String is used instead of boolean to prevent flipped bits
check_video_id = None
nextPageToken = 'start'
logMode = False

class SampleApp(Tk):
    __SECRETS_FILE = None
    @property
    def SECRETS_FILE(self):
        if self.__SECRETS_FILE is None:
            self.open_secrets_file()
        return self.__SECRETS_FILE

    __YOUTUBE = None
    @property
    def YOUTUBE(self):
        # Cache hit
        if self.__YOUTUBE is not None:
            return self.__YOUTUBE
        # Cache miss
        creds = None
        if os.path.exists(TOKEN_FILE_NAME):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE_NAME, scopes=YOUTUBE_READ_WRITE_SSL_SCOPE)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())    
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__SECRETS_FILE, scopes=YOUTUBE_READ_WRITE_SSL_SCOPE)
                creds = flow.run_local_server(port=0, authorization_prompt_message="Log in using the browser window.")
                # Save the credentials for the next run
            with open(TOKEN_FILE_NAME, 'w') as token:
                token.write(creds.to_json())
        return build(API_SERVICE_NAME, API_VERSION, credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
        

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.set_styles()
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, SingleVideoPage, CompleteChannelPage, PageHelp):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(PAGES[0])
        self.show_menu()

    def set_styles(self):
        self.title_font = tkfont.Font(
            family='Helvetica',
            size=18,
            weight='bold'
        )
        self.style = Style(self)
        self.style.configure('frame', background='white')

    def show_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Secrets file",
                             command=self.open_secrets_file)
        filemenu.add_command(label="Search video", command=self.search_video)
        filemenu.add_command(label="Search channel", command=self.search_channel)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_command(label="Help", command=self.show_help)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def open_secrets_file(self):
        self.__SECRETS_FILE = askopenfilename()



    def search_video(self):
        self.show_frame(PAGES[1])

    def search_channel(self):
        self.show_frame(PAGES[2])

    def show_help(self):
        self.show_frame(PAGES[3])

    
    @property
    def YOUTUBE():
        pass


class Page(Frame):
    title = "Page"

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        top_frame = Frame(self)
        if str(self).split('.!')[-1] != PAGES[0].lower():
            Button(
                top_frame,
                text="<",
                command=lambda: controller.show_frame(PAGES[0]),
                width=3
            ).pack(side='left', padx=5)
        Label(
            top_frame,
            text=self.title,
            font=controller.title_font
        ).pack(side='left', fill='x')
        top_frame.pack(side='top', fill='x')


class StartPage(Page):
    title = "This is the first page"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        button1 = Button(self, text="Search video",
                         command=lambda: controller.show_frame(PAGES[1]))
        button2 = Button(self, text="Search channel",
                         command=lambda: controller.show_frame(PAGES[2]))
        button1.pack()
        button2.pack()


class SingleVideoPage(Page):
    title = "Search single video"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        
        
        text = Label(self, text="""
        a
        b
        c
        """
        )

        text.pack(side='left')


class CompleteChannelPage(Page):
    title = "Search complete channel"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        text = Label(self, text="""
        a
        b
        c
        """
        )

        text.pack(side='left')


class PageHelp(Page):
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

class LoginPage(Page):
    title = "Login"

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        text = Label(self, text="""
        a
        b
        c
        """
        )

        text.pack(side='left')


if __name__ == '__main__':
    app = SampleApp()
    try:
        app.mainloop()
    except Exception as e:
        messagebox.showerror('Error', traceback.format_exc())
