@echo off
echo.
echo.   Updating from code repo
echo.
setlocal
set src=D:\GitHub\arcplus\ArcToolbox\Scripts

for %%a in (ungenerate.py clip_all_layers.py) do (
    echo copy /y "%src%\%%a" .\
    copy /y "%src%\%%a" .\
    )
rem ping -n 7 localhost >nul
goto :eof
