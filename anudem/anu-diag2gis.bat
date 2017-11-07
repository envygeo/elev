@echo off
:: Convert ANUDEM output files into formats readable by GIS

if "%1"=="" goto :Usage
setlocal enabledelayedexpansion
set dst=%1
set ogropt=-a_srs EPSG:3579
set compress=-co COMPRESS=LZW -co TILED=YES -co PREDICTOR=2
set gdalopt=-a_srs EPSG:3579 %compress%

call :renamer
call :RemoveEmpty
call :Specials
call :Main
call :Hillshade "%dst%"

endlocal
goto :eof

:: --------------------------------------------------------------------
:RemoveEmpty
  for %%a in (*.pnt, *.lin) do (
    call :check_size %%a 6 IS_OK
    if "!IS_OK!"=="False" call :run del %%a
    )
  goto :eof

:Specials
  if not exist "%dst%" mkdir "%dst%"
  for %%a in (*large_residual*.pnt, *contour_error*.pnt) do (
      call anu-special2vrt %%a
      call :run ogr2ogr %ogropt% -nlt point %dst% %%~na.vrt
      gzip %%a
      )
  goto :eof

:Main
    if not exist "%dst%" mkdir "%dst%"
    @for %%a in (*.flt, *.asc) do (
      if not exist %dst%\%%~na.tif (
        call :run gdal_translate %gdalopt% %%a %dst%\%%~na.tif
        )
      gzip %%a
      )

    @for %%a in (*.pnt) do (
      if not exist %dst%\%%~na.shp (
        call :run ogr2ogr %ogropt% -nlt point %dst% %%a
        gzip %%a
        )
			)

    @for %%a in (*.lin) do (
      if not exist %dst%\%%~na.shp (
        call :run ogr2ogr %ogropt% -nlt linestring %dst% %%a
        )
      gzip %%a
      )
    goto :eof

:Hillshade
	pushd %1
	for %%a in (*_dem.tif) do (
		set _fname=%%a
		set _fname=!_fname:~0,-8!_shade.tif
    if not exist !_fname! (
      call :run gdaldem hillshade %compress% %%a !_fname! -az 315 -alt 70
      )
		)
	popd
	goto :eof
	
:renamer
	REM echo on
	:: Humanize ANUDEM diagnostic file names
	set files=*.snk *.res *.ser *.per *.cer *.sto *.brk *.gpc *.gfc *.asp
	for %%a in (%files%) do call :do_rename %%a
	REM @echo off
	goto :eof
	
:do_rename
	if "%~x1"==".snk" rename "%1" "%~n1_sinks.pnt"
	if "%~x1"==".res" rename "%1" "%~n1_large_residuals.pnt"
	if "%~x1"==".ser" rename "%1" "%~n1_stream_errors.pnt"
	if "%~x1"==".per" rename "%1" "%~n1_polygon_errors.pnt"
	if "%~x1"==".cer" rename "%1" "%~n1_contour_errors.pnt"
	if "%~x1"==".sto" rename "%1" "%~n1_derived_streams.lin"
	if "%~x1"==".brk" rename "%1" "%~n1_break_lines.lin"
	if "%~x1"==".gpc" rename "%1" "%~n1_grid_point_codes.asc"
	if "%~x1"==".gfc" rename "%1" "%~n1_grid_flow.asc"
	if "%~x1"==".asp" rename "%1" "%~n1_grid_aspect.flt"
	goto :eof

:run
	:: Echo the command line to screen and then execute it.
	::
	:: Useful when you want to have echo turned off everywhere else,
	:: and not speckle code with `echo on && {cmd line here} && @echo off`
	set _cmd=%*
	echo !_cmd!
	!_cmd!
	if not !errorlevel!==0 (echo.*** Exit code: !errorlevel! && echo.)
	goto :eof

:Usage
    echo.
    echo.   Missing destination folder
    echo.
    echo.       %~0 path\to\output\shapes
    echo.
    goto :eof

:check_size
	:: Return True if file is greater than specified size (in bytes)
	::
	::		Arg1 = path\to\file.ext
	::		Arg2 = minimum acceptable byte size
	::  	Arg3 = variable name to set True/False
	::
	:: adapted from @Anders:
	:: 	How can I check the size of a file in a Windows batch script?
	:: 	http://stackoverflow.com/questions/1199645/
	:: and 
	:: http://www.dostips.com/DtTutoFunctions.php#FunctionTutorial.ReturningValuesViaReference
	setlocal
	set "file=%1"
	set "minbytesize=%2"

	FOR /F "usebackq" %%A IN ('%file%') DO set size=%%~zA

	if %size% LSS %minbytesize% (
		REM echo.	File is ^< %minbytesize% bytes
		endlocal
		set "%~3=False"
	) ELSE (
		REM echo.	File is ^>= %minbytesize% bytes
		endlocal
		set "%~3=True"
		)
	goto :eof