$python=(python --version)
if ([string]::IsNullOrEmpty($python)) {
    Exit
}

$arr = ".\build_env", ".\dist", ".\build", ".\bloodweb-clicker.exe"

for ($i=0; $i -lt $arr.Length; $i++) {
    if (Test-Path $arr[$i]) {
        Remove-Item $arr[$i] -Force -Recurse
    }
}

py -m venv build_env
.\build_env\Scripts\activate
py -m pip install -r requirements.txt
py -m pip install pyinstaller
pyinstaller --console --onefile .\bloodweb-clicker.py
deactivate
Move-Item -path .\dist\bloodweb-clicker.exe .\
Remove-Item .\build, .\dist, .\build_env -Force -Recurse
