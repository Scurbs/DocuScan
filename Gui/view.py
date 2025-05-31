import customtkinter as ctk

from customtkinter import filedialog
from tkinter import messagebox
from settings import *
from Gui.Widgets import Button
from tkinter import messagebox
from Gui.SettingsWindow import SettingsWindow


try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class FastDocuView(ctk.CTk):
    def __init__(self, is_light):
        super().__init__(fg_color=(WHITE, BLACK))
        self.is_light = is_light
        ctk.set_appearance_mode('light' if is_light else 'dark')
        
        window_width = 400
        window_height = 300

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.x = (self.screen_width // 2) 
        self.y = (self.screen_height // 2) - (window_height // 2)

        self.geometry(f'{window_width}x{window_height}+{self.x}+{self.y}')
        self.resizable(False, False)
        self.title('FastDocu')
        
        self.title_bar_color(is_light)
        
        self.controller = None
        self.filepath = None
        self.settings_window = None

        self.rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform='a')
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight=1, uniform='a')

        self.button_select = Button(self, 0, 0, 1, 1, '', 'Select File', 
                                    lambda: self.select_path_dialog("Select a PDF File", FILETYPES))
        self.button_convert = Button(self, 1, 0, 1, 1, '', 'Convert', 
                                     lambda: self.convert())
        self.button_settings = Button(self, 2, 0, 1, 1, '', 'Settings', 
                                      lambda: self.open_settings_window())

    def title_bar_color(self, is_light):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['light'] if is_light else TITLE_BAR_HEX_COLORS['dark']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

    def set_controller(self, controller):
        self.controller = controller
    
    def select_path_dialog(self, title, filetypes):
        self.filepath = filedialog.askopenfilename(title=title, filetypes=filetypes)
        
    def open_settings_window(self):
        if self.settings_window is None or not self.settings_window:
            
            self.settings_window = SettingsWindow(self, self.is_light, self.controller)
            self.settings_window.attributes("-topmost", False)
        else:
            
            self.settings_window.focus()
            self.settings_window.lift()
            self.settings_window.attributes("-topmost", False)
            
    def convert(self):
       
        if self.filepath:
            self.controller.convert(self.filepath)
        else:
            messagebox.showinfo("Info","Please select a file before converting")          



