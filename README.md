# ImageProcessor

ImageProcessor is a Python GUI application for processing images.

### Prerequisites

Before you start installation make sure you have installed `python3` and `virtualenv` and these commands are available
from terminal.<br>
You must have python version >=3.6 && <=3.9 and use Windows OS.

### Installation

1. Clone the repository
1. Navigate to the project root directory using terminal
1. Create virtual environment
1. Activate virtual environment
1. Run `pip install -r requirements.txt` to install project dependencies

### Deploying

Use the [PyInstaller](https://pyinstaller.org/en/stable/) with the "main.spec" file to build portable executable.

From the activated virtual environment run:
```bash
pyinstaller main.spec
```