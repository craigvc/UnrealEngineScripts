# Unreal Plugin Builder

A simple GUI tool for building Unreal Engine plugins using RunUAT.

## Features
- Select the Unreal Engine installation folder.
- Choose a plugin (.uplugin) file to build.
- Define the output folder for the packaged plugin.
- Select the target platform (Win64, Mac, Linux, Android, iOS).
- Optional flags: Clean build, No Compile, Verbose Output.
- Runs `RunUAT.bat` on Windows and `RunUAT.sh` on Linux/Mac.
- Updates the Engine Version in the `.uplugin` file automatically.

## Requirements
- Python 3.x (includes Tkinter by default on Windows and Mac)
- Unreal Engine installed with `RunUAT.bat` or `RunUAT.sh`
- Tkinter (pre-installed with Python, but may need manual installation on Linux)
- Python 3.x
- Unreal Engine installed with `RunUAT.bat` or `RunUAT.sh`
- Tkinter (for GUI)

## Installation (Windows)
### 1. Install Python
Download and install the latest version of Python from [python.org](https://www.python.org/downloads/). Make sure to check the box **"Add Python to PATH"** during installation.

### 2. Install Dependencies

#### Linux Users: Install Tkinter if missing
If you are on Linux and Tkinter is not installed, run the following command:

**Ubuntu/Debian:**
```sh
sudo apt-get install python3-tk
```

**Fedora:**
```sh
sudo dnf install python3-tkinter
```

**Arch Linux:**
```sh
sudo pacman -S tk
```
Clone the repository:
```sh
git clone <repo-url>
cd <repo-folder>
```

Install required dependencies:
```sh
pip install tk
```

## Usage
Run the script:
```sh
python plugin_builder.py
```

## Instructions
1. Select your **Unreal Engine root folder** (e.g., `I:/5.5`).
2. Choose the **.uplugin file** of the plugin you want to build.
3. Select the **output folder** where the packaged plugin will be stored.
4. Choose the **target platform** from the dropdown.
5. Check any **optional flags** if needed.
6. Click **Build Plugin** to start the process.

## Troubleshooting
- **Target platform not saving**: Ensure the target platform is correctly wrapped in quotes. If the issue persists, try manually specifying it in the `.uplugin` file.
- **Missing RunUAT**: Ensure you selected the correct Unreal Engine installation.
- **Permission Denied (Linux/Mac)**: Run `chmod +x RunUAT.sh` inside `Engine/Build/BatchFiles/`.
- **AutomationTool errors**: Verify your Unreal Engine installation.

## Disclaimer
This tool has been primarily tested on **Windows**. It **should** work on Linux and Mac, but has not been fully tested on those platforms. If you encounter issues on non-Windows systems, manual adjustments may be needed.

## License
This project is open-source and available under the MIT License.

