from json.decoder import JSONDecodeError
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
from pages.start_page import *
from pages.video_page import *
from pages.channel_page import *
from pages.login_page import *
from pages.help_page import *



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
    PAGES = (
        StartPage,
        VideoPage,
        ChannelPage,
        LoginPage,
        HelpPage
    )
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
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE_NAME, scopes=YOUTUBE_READ_WRITE_SSL_SCOPE)
            except Exception:
                # Remove token if invalid
                os.remove(TOKEN_FILE_NAME)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())    
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.SECRETS_FILE, scopes=YOUTUBE_READ_WRITE_SSL_SCOPE)
                    creds = flow.run_local_server(port=0, authorization_prompt_message="Log in using the browser window.")
                except JSONDecodeError as e:
                    self.show_error(message="Credentials are not in JSON format.", exception=e)
            # Save the credentials for the next run
            with open(TOKEN_FILE_NAME, 'w') as token:
                token.write(creds.to_json())
        return build(API_SERVICE_NAME, API_VERSION, credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
    
    __USER__ = None
    @property
    def USER(self):
        # Cache hit
        if self.__USER__ is not None:
            return self.__USER__
        # Cache miss
        results = self.fetch()
        channel_id = results["items"][0]["id"]
        try:
            channel_title = results["items"][0]["snippet"]["title"]
        except Exception as e:
            self.show_error('Channel info could not be obtained')
        self.__USER__ = (channel_id, channel_title)
        return self.__USER__
        
    def convert_comment_id_to_video_id(comment_id):
        return vidIdDict[comment_id]
        
    def fetch_channels(self, part='snippet', fields='items/id,items/snippet/title'):
        return self.YOUTUBE.channels().list(
            part=part, #Can also add "contentDetails" or "statistics"
            mine=True,
            fields=fields
        ).execute()

    def filter_video_id(self, video_string):
        """Returns the video id"""
        for pattern in [
            r'.*(?:youtube(?:-nocookie)?\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=)|youtu\.be/)([^"&?/\s]{11})',
            r'.*([^"&?/\s]{11})'
        ]:
            youtube_regex_match = re.match(
                pattern,
                video_string,
                flags=re.DOTALL+re.IGNORECASE
            )
            if youtube_regex_match:
                return youtube_regex_match.group(1)
        raise Exception('Video id not found.')

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.set_styles()
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in self.PAGES:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_first_frame()
        self.build_menu()

    def set_styles(self):
        self.title_font = tkfont.Font(
            family='Helvetica',
            size=18,
            weight='bold'
        )
        self.style = Style(self)
        self.style.configure('frame', background='white')

    def build_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Authenticate",
                             command=self.authenticate)
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

    def show_first_frame(self):
        self.show_frame(self.PAGES[0].__name__)

    def open_secrets_file(self):
        self.__SECRETS_FILE = askopenfilename(title="Please select your json credentials")

    def authenticate(self):
        """Just calling YOUTUBE calls the logic to authenticate"""
        self.YOUTUBE
    
    def get_user(self):
        results = self.YOUTUBE.channels().list(
            part="snippet", #Can also add "contentDetails" or "statistics"
            mine=True,
            fields="items/id,items/snippet/title"
        ).execute()
        return results

    def get_channel_id(self, video_id):
        results = self.YOUTUBE.videos().list(
            part="snippet",
            id=video_id,
            fields="items/snippet/channelId",
            maxResults=1
        ).execute()
        
        channel_id = results["items"][0]["snippet"]["channelId"]

        return channel_id

    def search_video(self):
        self.show_frame('VideoPage')

    def search_channel(self):
        self.show_frame('ChannelPage')

    def show_help(self):
        self.show_frame('HelpPage')

    def show_error(self, title="Error", message=traceback.format_exc(), exception=None):
        """Shows an error popup, stops execution if there is an exception"""
        messagebox.showerror(title, message)
        if exception:
            raise Exception() from exception
    
    def show_info(self, title="Info", message=None):
        """Shows an info popup"""
        messagebox.showinfo(title, message)

    def ask(self, title="Warning", message=''):
        return messagebox.askquestion(title, message, icon='warning')

if __name__ == '__main__':
    app = SampleApp()
    app.mainloop()
