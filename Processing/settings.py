import sys
import os

if getattr(sys, 'frozen', False):
   
    BASE_PATH  = os.path.dirname(sys.executable)
    
else:
    BASE_PATH  = r'C:\Users\janes.pozar\Desktop\FastDocu'

EQUIPMENT_FILE = os.path.join(BASE_PATH,'assets','json','equipment.json')
TESSERACT_PATH = os.path.join(BASE_PATH , 'Tesseract-OCR', 'tesseract.exe')
TITLE_SHEET = os.path.join(BASE_PATH,'assets','titlesheet.xlsx')
CONFIG_OCR = '--psm 6 --oem 3 eng'

VERSION = "2.1"

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
RESET = '\033[0m'


SCANNING_COLOR = '#75d19d'
ERROR_COLOR = '#ff6b4a'

U_METER = '\u03BCm'

BLACK = '#000000'
WHITE = '#EEEEEE'

TITLE_BAR_HEX_COLORS = {
    'dark': 0x00000000,
    'light': 0x00EEEEEE
}

MAIN_ROWS = 4
MAIN_COLUMNS = 1

SETTINGS_ROWS = 4
SETTINGS_COLUMNS = 3

EQUIPMENT_COLUMNS = 3
EQUIPMENT_ROWS = 2


FILETYPES = [("PDF files", "*.pdf"), ("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")]
DEFAUL_DPI = 300

EQUIPMENT_START_COLUMN = 27

