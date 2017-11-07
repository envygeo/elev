@echo off
:: --- Run.bat ---
:: Echo the command line to screen and then execute it.
::
:: Useful when you want to have echo turned off everywhere else,
:: and not speckle code with `echo on && {cmd line here} && @echo off`
setlocal enabledelayedexpansion
echo === Run =================
set _cmd=%*
echo !_cmd!
call !_cmd!
if not !errorlevel!==0 (echo.*** Non-zero exit code: !errorlevel!)
echo =========================
endlocal
