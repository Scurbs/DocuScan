import fitz  
from PIL import Image, ImageFilter
import os
from multiprocessing import Pool
import time


def process_page(page_number, pdf_path, output_folder, dpi):
    try:
        start_time = time.time()
        document = fitz.open(pdf_path)
        page = document.load_page(page_number)
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = img.filter(ImageFilter.SHARPEN)

        image_path = os.path.join(output_folder, f"page{page_number + 1}.jpg")
        img.save(image_path, dpi=(dpi, dpi), quality=95, optimize=True)
        img.close()
        document.close()

        print(f"Page {page_number + 1} processed in {time.time() - start_time:.2f} seconds.")
    except Exception as e:
        print(f"Failed to process page {page_number + 1}: {str(e)}")

class PDFToImagesConverter:
    """
    A class to convert PDF pages to images.
    """
    def __init__(self, pdf_path, output_folder, dpi):
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.dpi = dpi

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def convert(self):

        try:
            start_time = time.time()
            document = fitz.open(self.pdf_path)
            num_pages = len(document)
            document.close()

            print(f"Starting conversion of {num_pages} pages.")

            args = [(page_number, self.pdf_path, self.output_folder, self.dpi) for page_number in range(num_pages)]

            #Multiprocessing for faster conversion to img
            with Pool() as pool:
                pool.starmap(process_page, args)

            print(f"PDF conversion completed in {time.time() - start_time:.2f} seconds.")
        except Exception as e:
            print(f"Failed to convert PDF: {str(e)}")
