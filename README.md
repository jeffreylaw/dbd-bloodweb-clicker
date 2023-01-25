# dbd-bloodweb-clicker
https://user-images.githubusercontent.com/21249877/214710260-c31dbdd3-8aec-4c78-bb34-9f90df08a1a5.mp4
## General
- Limited testing done on 1920x1080 full screen DBD on Windows 10 
- USE AT YOUR OWN RISK
- To get the executable, visit [here](https://github.com/jeffreylaw/dbd-bloodweb-clicker/releases/latest) and click on bloodweb-clicker.exe to download

## Usage

### Running using Python
Prequisites: Python 3
1. `py -m venv env`
2. `.\env\Scripts\activate`
3. `py -m pip install -r requirements.txt`
4. `py .\bloodweb-clicker.py`
5. Switch to DBD bloodweb screen
6. Press right-control button on keyboard to exit

### Running using executable
1. Run bloodweb-clicker.exe
2. Switch to DBD bloodweb screen
3. Press right-control button on keyboard to exit

## Limitations & Bugs
- Prestiging does not work

## Planned Features
- Prioritizing certain nodes
- Checking if there are bloodpoints left
- Optimize circle detection

## Building
### Manual building
Prequisites: Python 3
1. `py -m venv env`
2. `.\env\Scripts\activate`
3. `py -m pip install -r requirements.txt`
4. `py -m pip install pyinstaller`
5. `pyinstaller --clean --console --onefile .\bloodweb-clicker.py`

### Alternative using Powershell script (untested)<br>
Prequisites: Python 3
1. Run `.\build.ps1` in Powershell<br>
Note: You may need to modify your settings to allow PowerShell script executions. [https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.3]<br>
