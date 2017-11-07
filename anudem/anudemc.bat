@if "%1"=="" goto :usage
@echo %DATE% %TIME% > %~n1.log
if not exist "%~n1n" mkdir "%~n1"
start /b "Anudem" %~dp0\Anudem53\bin\anudemc.exe <%1 >> %~n1.log 2>&1
@start /b "Anudem log" tail -c +1 -f %~n1.log
@goto :eof

:usage
	echo.
	echo.	%~n0 [anudem_command_file.ext]
	echo.
	goto :eof