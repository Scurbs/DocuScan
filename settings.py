import sys
import os

if getattr(sys, 'frozen', False):
     # Path where the .exe is located when bundled 
    BASE_PATH  = os.path.dirname(sys.executable)
    
else:
    BASE_PATH  = r"E:\Git_Workspace\DocuScan"
TESSERACT_PATH = os.path.join(BASE_PATH , 'Tesseract-OCR', 'tesseract.exe')

CONFIG_OCR = '--psm 6 --oem 3 eng'

VERSION = "2.1"

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'

RECOVERY_COLOR = '#fcc135'
RAUMKLASSE_COLOR = '#3db5f5'
SCANNING_COLOR = '#75d19d'
INTEGRAL_COLOR = '#d661fa'
ERROR_COLOR = '#ff6b4a'

U_METER = '\u03BCm'

BLACK = '#000000'
WHITE = '#EEEEEE'

TITLE_BAR_HEX_COLORS = {
    'dark': 0x00000000,
    'light': 0x00EEEEEE
}

MAIN_ROWS = 3
MAIN_COLUMNS = 1

SETTINGS_ROWS = 4
SETTINGS_COLUMNS = 3

FILETYPES = [("PDF files", "*.pdf"), ("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")]
DEFAUL_DPI = 300



