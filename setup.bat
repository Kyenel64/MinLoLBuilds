:: Check for Python Installation
python --version 3>NUL
if errorlevel 1 goto errorNoPython

pip install requests
pip install pillow
pip install BeautifulSoup4
pip install cssutils

IF EXIST ".config" (
    echo Complete 
) ELSE (
    python ./main.py
)
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed