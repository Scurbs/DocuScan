from settings import *
import customtkinter as ctk
from Gui.Widgets import  Button
from tkinter import messagebox


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, is_light,controller):
        super().__init__(master = parent, fg_color=(WHITE, BLACK))
        self.is_light = is_light
        self.parent = parent
        self.title("Settings")
        self.geometry('500x200')
        self.controller = controller
        self.rowconfigure(list(range(SETTINGS_ROWS)),weight=1,uniform='a')
        self.columnconfigure(list(range(SETTINGS_COLUMNS)),weight=1,uniform='a')
        ctk.set_appearance_mode('light' if is_light else 'dark')
        self.dpi = self.controller.get_dpi()
        self.radio_state = ctk.IntVar(value=3)
        self.button_save_dpi = Button(self,1,1,1,1,'',"Speichere DPI",self.save_dpi)
        self.button_default_values = Button(self,2,1,1,1,'',"Default Werte",self.set_default_values)

        self.dpi_textfield = ctk.CTkEntry(self,corner_radius=5,bg_color="White",placeholder_text=self.dpi)
        self.dpi_textfield.grid(column = 1, row = 0)
    
        self.debug_full_radio_button = ctk.CTkRadioButton(self,text="Debug Mode",command=lambda: self.set_debug_mode(1),variable=self.radio_state,value=1)
        self.debug_not_radio_button = ctk.CTkRadioButton(self,text="No Debug",command=lambda: self.set_debug_mode(0),variable=self.radio_state,value=2)
        self.debug_full_radio_button.grid(column = 0, row = 3)
        self.debug_not_radio_button.grid(column = 1, row = 3)

        self.closing_button = Button(self, text="Close",row = 4, column= 1, command= self.close_window)

    def close_window(self):
        print("Quit settings window")
        self.destroy()
        self.parent.settings_window = None

    def set_debug_mode(self, mode):
        self.controller.set_debug_mode(mode)
                
    def save_dpi(self):       
        try:
            self.dpi = int(self.dpi_textfield.get())
            if 200 < self.dpi < 600:
                self.controller.save_dpi(self.dpi)
            else:
                messagebox.showinfo("Info","Number must be between 200 and 600")
        except:
            messagebox.showinfo("Info", "Input must be a number")

    def set_default_values(self):
        
        self.controller.save_dpi(DEFAUL_DPI)

    def get_dpi(self):
        return self.dpi

