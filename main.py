from Programm.model import FastDocuModel
from Gui.view import FastDocuView
from Programm.controller import FastDocuController

import multiprocessing

if __name__ == "__main__":
    
    multiprocessing.freeze_support()
    model = FastDocuModel()
    view = FastDocuView(False)
    controller = FastDocuController(model, view)
    view.mainloop()
    
    
