import threading
class FastDocuController:
    def __init__(self, model, view):
        self.model = model
        
        self.view = view
        self.view.set_controller(self)  
       

    def set_default_values(self):
        print("Set default values")


    def save_dpi(self,dpi):    
        self.model.save_dpi(dpi)

    def convert(self, filepath):
        self.filepath = filepath
        threading.Thread(target=self.model.run_convert, args=(filepath,)).start()

    def get_dpi(self):
        dpi = self.model.get_dpi()
        return dpi

    def set_debug_mode(self, debug_mode = 0):
        
        self.model.set_debug_mode(debug_mode)

    
