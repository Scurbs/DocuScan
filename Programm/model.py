import os
import re
import shutil
from settings import *
from Processing.PdfToImages import PDFToImagesConverter
import time




class FastDocuModel:
    def __init__(self):
        self.dpi = 300
        self.debug_mode = 0
        self.output_folder = "output_images"
        self.base_path = BASE_PATH
        self.set_debug_mode()

    def save_dpi(self, dpi):

        if not dpi:
            self.dpi = DEFAUL_DPI
        else:
            self.dpi = dpi
        print(f"DPI set to: {self.dpi}")
        
    def get_dpi(self):

        return self.dpi
    
    def set_debug_mode(self, debug_mode=0):

        self.debug_mode = debug_mode
        if debug_mode == 1:
            print("Debug mode is set")
        if debug_mode == 0:
            print("Debug mode is not set")

    def extract_page_number(self, filename):

        match = re.search(r'page(\d+)', filename)
        if match:
            return int(match.group(1))
        return float('inf')  
    
    def run_convert(self, filepath):
       

        self.filepath = filepath
        self.output_folder = "output_images"
         
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        else:
            shutil.rmtree(self.output_folder)
            os.makedirs(self.output_folder)
        
      
        self.converter = PDFToImagesConverter(self.filepath,self.output_folder,self.dpi)

        self.converter.convert()
               
        filenames = [f for f in os.listdir(self.output_folder) if os.path.isfile(os.path.join(self.output_folder, f))]

        filenames.sort(key=self.extract_page_number)
        print(filenames)
        print("All pages converted to images")
       