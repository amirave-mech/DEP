for /f "delims=" %%i in ('pip show pyautogui 2^>^&1 ^| findstr WARNING') do set installed=%%i
if defined installed (
    py -m pip install pyautogui
)
cd dep_web
call npm install >nul
start /B npm start
cd ..
timeout /t 1 >nul
python open_web.py