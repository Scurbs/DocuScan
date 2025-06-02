import customtkinter as ctk

from customtkinter import filedialog
from tkinter import messagebox
from settings import *
from Programm.model import UpdateType
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

    def update(self, update_type, data=None, text = None):
        
        if update_type == UpdateType.TASK_STARTED:

            self.after(0, self.open_progress_bar) 
           
        elif update_type == UpdateType.TASK_PROGRESS:

            print("Status:", data,"%,", text)
            self.after(0, self.update_progress_bar, data, text) 

        elif update_type == UpdateType.TASK_COMPLETED:

            self.after(0, lambda: messagebox.showinfo("Notification", "Finished data extraction"))  
            self.after(0, self.close_progress_window)
            

        elif update_type == UpdateType.ERROR_OCCURRED:

            self.after(0, lambda: messagebox.showerror("Error", text))  
            self.after(0, self.close_progress_window)  

    def update_progress_bar(self, value, text):
        
        if hasattr(self, 'progress_bar'):
            self.progress_bar.set(value/100)  
            self.progress_label.configure(text = text)
            self.progess_percent_label.configure(text = f'{value}%')
        else:
            print("Progress bar not initialized") 

    def close_progress_window(self):
        if hasattr(self, 'progress_window'):
            self.progress_window.destroy()  
            self.progress_window = None 

    def open_progress_bar(self):
        # Create the progress window
        self.progress_window = ctk.CTkToplevel(master=self, fg_color=(WHITE, BLACK))
        self.progress_window.resizable(False, False)
        
        window_width = 350
        window_height = 60

        screen_width = self.progress_window.winfo_screenwidth()
        screen_height = self.progress_window.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.progress_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.progress_window.title("Progress")
        self.progress_window.lift()
        self.progress_window.attributes("-topmost", True)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_window, width=300, mode="determinate")
        self.progress_bar.set(0)
        self.progress_bar.grid(row=0, column=0, rowspan=2, sticky="ew", padx=5, pady=5)

        self.progress_label = ctk.CTkLabel(master=self.progress_window, text_color="White", height=5, text="Initialize parameters")
        self.progress_label.grid(row=2, column=0, sticky="s", padx=5, pady=5)

        self.progess_percent_label = ctk.CTkLabel(master=self.progress_window, text_color="White", text="", height=5)
        self.progess_percent_label.grid(row=0, column=2, sticky="e", padx=5, pady=5)


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



