# FastDocu

The program extracts data from measurement strips contained within a PDF and converts it into an Excel file. The process involves first converting the PDF pages into images, then using OCR (Optical Character Recognition) through Pytesseract to extract the data.

## Table of Contents

- [Installation](#installation)
- [Description](#description)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Description
DocuScan allows users to process measurement equipment data with associated measuring dates directly from a PDF. The program includes options to set DPI for the PDF-to-image conversion (recommended to match the DPI of the scanner or printer for accuracy). After selecting the desired PDF and pressing "Convert," the program scans all measurement strips within the document.
Each page from the PDF is converted into an individual sheet in an Excel file.
## Installation

To get a .exe follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Scurbs/DocuScan.git

2. Install dependencies:

   For good practice it is recommended to use a virtual environment
   ```
   pip install -r requirements.txt
   ```
4. Install Tesseract for Windows:

   Download **[Tesseract](https://github.com/UB-Mannheim/tesseract)** from UB-Mannheim for Windows
   Place the folder "Tesseract" into the same folder where main.py is.

3. Edit DocuScan.spec:
   If you want to use the debug mode fully, then you have to set the flag on true for console

5. Run the main.spec file for building the .exe
   ```
   pyinstaller DocuScan.spec
   ```
6. Place the .exe in the same folder where main.py is.
   You can now use the program !
## Usage
### Start
The Start page offers four main options:

- Select File: Choose a PDF file to process.
- Convert: Begin converting the selected PDF to an Excel file.
- Settings: Adjust conversion and debugging settings.
### Settings
Under Settings, set the DPI (recommended to match the DPI of your scanner or printer) for accurate conversion of PDF pages to images. You can also enable Debug Mode, which opens a console to display debug statements during the conversion process 
### Convert
Ensure a file is selected before starting the conversion process. Once selected, press "Convert" to begin transforming the PDF into an Excel file.
### Excel Output

The generated Excel file includes:

- Timestamp: From each measurement there is the according timestamp
- Particle size: For each measuring stripe there a two colums for the particle size 0.5µm and 0.3µm
- Serial Number: The serial number for each measuring stripe is also displayed
- The mean values for each particle size
- Checks if the value is within a range of 15%
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

### Acknowledgements
This project utilizes the following third-party tools:
- **[pytesseract](https://github.com/madmaze/pytesseract)**: A Python wrapper for Tesseract OCR, licensed under the Apache License 2.0.
- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)**: An OCR engine developed by Google, also licensed under the Apache License 2.0.

Please note that by using this project, you must also comply with the terms of the Apache License 2.0 for `pytesseract` and Tesseract OCR. A copy of the Apache License is available [here](https://www.apache.org/licenses/LICENSE-2.0).


## Contact
Created by Janes Pozar & Avdo Muminovic. For additional questions, please reach out through janes.pozar@students.fhnw.ch or visit the project repository.

