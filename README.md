# ImageProcessor

ImageProcessor is a Python GUI application for processing images.

### Prerequisites

Before you start installation make sure you have installed `python3` and `virtualenv` and these commands are available
from terminal.<br>
You must have python version >=3.6 && <=3.9 and use Windows OS.

### Installation

1. Clone the repository.
2. Navigate to the project root directory using terminal.
3. Create virtual environment.
4. Activate virtual environment.
5. Run `pip install -r requirements.txt` to install project dependencies.
6. (Optional) To have a working OCR, install 3rd party tesseract executable from [here](https://github.com/UB-Mannheim/tesseract/wiki) and add executable path to the .env .
7. (Optional) To have an object detection capabilities, you can download "SSD MobileNet V2" from [here](https://gist.github.com/qianlin404/c7991048c5f3264ce13d520ce0274493), unpack and add neural network's "model", "config" and "label" file paths in the .env or download any object detection neural network, which was made with the Tenserflow.  

### Deployment

Use the [PyInstaller](https://pyinstaller.org/en/stable/) with the "main.spec" file to build portable executable.

From the activated virtual environment terminal run:
```bash
pyinstaller main.spec
```