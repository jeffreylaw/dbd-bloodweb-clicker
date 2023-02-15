# dbd-bloodweb-clicker
https://user-images.githubusercontent.com/21249877/214710260-c31dbdd3-8aec-4c78-bb34-9f90df08a1a5.mp4
## General
- Developed for educational purposes only.
- Supports and tested on [1920x1080 full screen DBD on Windows 10] only.
- USE AT YOUR OWN RISK. Although Behaviour doesn't actively ban for macroing (except bots), any third party software can trigger their anti-cheating software. You have been warned. (https://forums.bhvr.com/dead-by-daylight/discussion/82667/will-struggle-macros-get-you-banned)
- To get the executable, visit [here](https://github.com/jeffreylaw/dbd-bloodweb-clicker/releases/latest) and click on bloodweb-clicker.exe to download

## Usage

### Running using Python
Prequisites: Python 3
1. `py -m venv env`
2. `.\env\Scripts\activate`
3. `py -m pip install -r requirements.txt`
4. `py .\bloodweb-clicker.py`
5. Switch to DBD bloodweb screen

### Running using executable
1. Run bloodweb-clicker.exe
2. Switch to DBD bloodweb screen

### Resume, Pause, and Quit script
- F1 key -> Resume
- F2 key -> Pause
- F4 key -> Quit script

## Limitations & Bugs
- Prestiging may not work

## Planned Features
- None at this time

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
You may need to modify your settings to allow PowerShell script executions. [https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.3]<br>
