@echo off
if "%1"=="all" (goto :Standard) else (
  call :run python %~dp0\build-anudem-args-file.py %*
  )
goto :eof

:: --------------------------------------------------------------------
:Standard
  :: build all standard cell sizes
  for %%a in (100 75 50 40 30 25 20 15) do (
    call :run python %~dp0\build-anudem-args-file.py . %%a selection_buffer_3000m
    )
  goto :eof

:run
	:: Echo the command line to screen and then execute it.
	::
	:: Useful when you want to have echo turned off everywhere else,
	:: and not speckle code with `echo on && {cmd line here} && @echo off`
  setlocal enabledelayedexpansion
	set _cmd=%*
	echo ====================
  echo !_cmd!
	!_cmd!
	if not !errorlevel!==0 (echo.*** Exit code: !errorlevel! && echo.)
  endlocal
	goto :eof
