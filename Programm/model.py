import os
import re
import shutil
from Processing.OCRProcessor import OCRProcessor
from settings import *
from Processing.PdfToImages import PDFToImagesConverter
from Processing.ExcelExporter import Exporter
from enum import Enum
import time


class UpdateType(Enum):
    TASK_STARTED = "task_started"
    TASK_PROGRESS = "task_progress"
    TASK_COMPLETED = "task_completed"
    ERROR_OCCURRED = "error_occurred"
    

class FastDocuModel:
    def __init__(self):
        self.dpi = 300
        self.debug_mode = 0
        self.output_folder = "output_images"
        self.all_results = []
        self.tesseract_path = TESSERACT_PATH
        self.config_ocr = CONFIG_OCR
        self.base_path = BASE_PATH
        self._observers  =[]
        self.set_debug_mode()
       

    def add_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, update_type, data=None, text = None):
        for observer in self._observers:
            observer.update(update_type, data, text)

    def save_dpi(self, dpi):
        """Set the DPI for image processing."""
        if not dpi:
            self.dpi = DEFAUL_DPI
        else:
            self.dpi = dpi
        print(f"DPI set to: {self.dpi}")
        
    def get_dpi(self):
        """Return the current DPI."""
        return self.dpi
    
    def set_debug_mode(self, debug_mode=0):
        """Set the debug mode for OCR processing."""
        self.debug_mode = debug_mode
        if debug_mode == 1:
            print("Debug mode is set")
        if debug_mode == 0:
            print("Debug mode is not set")

    def extract_page_number(self, filename):
        """Extract the page number from a filename.

        This function assumes filenames are in a format like "page1.png", "page10.png", etc.
        """
        match = re.search(r'page(\d+)', filename)
        if match:
            return int(match.group(1))
        return float('inf')  
    
    def run_convert(self, filepath):
        """Convert a PDF to images and process each page using OCR."""
        self.notify_observers(UpdateType.TASK_STARTED,0,"")
        time.sleep(1)
        self.notify_observers(UpdateType.TASK_PROGRESS, 0,"Initialize parameters")
        self.filepath = filepath
        self.output_folder = "output_images"
        self.all_results = [] #Clearing List for new data

        self.notify_observers(UpdateType.TASK_PROGRESS, 5,"Convert PDF to Images")
         
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        else:
            shutil.rmtree(self.output_folder)
            os.makedirs(self.output_folder)
        
      
        self.converter = PDFToImagesConverter(self.filepath,self.output_folder,self.dpi)

        self.notify_observers(UpdateType.TASK_PROGRESS, 10,"Extract Values from measuring stripe")
        self.converter.convert()
               
        filenames = [f for f in os.listdir(self.output_folder) if os.path.isfile(os.path.join(self.output_folder, f))]

        filenames.sort(key=self.extract_page_number)

        self.notify_observers(UpdateType.TASK_PROGRESS, 15,"Preparing pages")
        time.sleep(1)
        for page_count, filename in enumerate(filenames, start=1):
            self.outputfolder_path = os.path.join(self.output_folder, filename)

            try:
                print("Open OCR Processor")
                processor = OCRProcessor(self.tesseract_path, self.base_path, self.config_ocr, self.debug_mode)
                result = processor.process_image_for_ocr(self.outputfolder_path, page_count)
                
                self.all_results.extend(result)

                progress_pages = 100 / len(filenames) * page_count
                
                self.notify_observers(UpdateType.TASK_PROGRESS, int(progress_pages),f"Extracting values from page {page_count}")
                print(f'{GREEN} FINISHED PAGE {page_count}{RESET}')
            except Exception as e:
                print(f"Error processing page {page_count}: {e}")
        self.notify_observers(UpdateType.TASK_PROGRESS, 85,"Writing dato to Excel")
        self.exporter = Exporter(
            input_data_list=self.all_results,
            notify_observer=self.notify_observers,
            UpdateType=UpdateType,
            excel_filename="output.xlsx",
            debug_mode=self.debug_mode
        )
        self.exporter.handle_process()  
        self.notify_observers(UpdateType.TASK_COMPLETED,100,"Finished extracting values from measuring stripes")
        
    
    def get_all_results(self):
        """Return all the OCR results collected from processed images."""
        return self.all_results