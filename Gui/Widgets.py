import customtkinter as ctk

class Button(ctk.CTkButton):
    def __init__(self, 
                 parent, 
                 row, 
                 column, 
                 rowspan=1, 
                 columnspan=1, 
                 anchor="center",  
                 text="Button",    
                 command=None,
                 padx = 5,
                 pady = 5,
                 sticky = "",    
                 **kwargs):        
        super().__init__(master=parent, text=text, command=command,**kwargs)

       
        self.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=sticky,
            pady = pady,
            padx = padx 
        )

class Label(ctk.CTkLabel):
    def __init__(self, 
                 master,
                 row,
                 column,
                 rowspan=1,
                 columnspan=1,
                 width=0, 
                 height=28, 
                 corner_radius=None, 
                 bg_color="transparent", 
                 fg_color=None, 
                 text_color=None, 
                 text_color_disabled=None, 
                 text="CTkLabel", 
                 font=None, 
                 image=None, 
                 compound="center", 
                 anchor="center", 
                 wraplength=0, 
                 padx = 5,
                 pady = 5,
                 **kwargs):
        super().__init__(master=master, 
                         width=width, 
                         height=height, 
                         corner_radius=corner_radius, 
                         bg_color=bg_color, 
                         fg_color=fg_color, 
                         text_color=text_color, 
                         text_color_disabled=text_color_disabled, 
                         text=text, 
                         font=font, 
                         image=image, 
                         compound=compound, 
                         anchor=anchor, 
                         wraplength=wraplength, 
                         **kwargs)
        # Use grid with the provided row and column attributes
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan,padx=padx,pady=pady)

class EntryField(ctk.CTkEntry):
    def __init__(self, 
                 master,
                 row,
                 column,
                 rowspan=1,
                 columnspan=1,
                 width=140, 
                 height=28, 
                 corner_radius=None, 
                 border_width=None, 
                 bg_color="transparent", 
                 fg_color=None, 
                 border_color=None, 
                 text_color=None, 
                 placeholder_text_color=None, 
                 textvariable=None, 
                 placeholder_text=None, 
                 font=None,
                 padx = 5,
                 pady = 5, 
                 sticky ="", 
                 **kwargs):
        # Initialize the CTkEntry with the provided parameters
        super().__init__(master=master,
                         width=width, 
                         height=height, 
                         corner_radius=corner_radius, 
                         border_width=border_width, 
                         bg_color=bg_color, 
                         fg_color=fg_color, 
                         border_color=border_color, 
                         text_color=text_color, 
                         placeholder_text_color=placeholder_text_color, 
                         textvariable=textvariable, 
                         placeholder_text=placeholder_text, 
                         font=font, 
                         **kwargs)
        
        # Use grid with the provided row and column attributes
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan,padx = padx, pady = pady,sticky = sticky)