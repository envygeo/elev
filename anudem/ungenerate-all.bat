@echo off
:: Export feature classes to ArcInfo GENERATE format
::
:: Project: ytdemv3
:: 2015-Feb-12, matt.wilkie@gov.yk.ca
setlocal
set ungen=D:\b\code\arcplus\ArcToolbox\Scripts\ungenerate.py

set src=%1
if "%1"=="default" set src=clipped.gdb
if not exist "%src%" goto :Usage

set noZ=selection_buffer_3000m
REM ::NHN
set Z=contour_imperial, contour_metric, Joined_NHN_waterbody_v4_Lake_Z, point_imperial, point_metric, NHN_Lakes_lines_with_Z_median
set lakes=NHN_HD_WATERBODY_2
set streams=NHN_HN_PrimaryDirectedNLFlow_1
::canvec+
REM set Z=contour_imperial, contour_metric, cvplus_Lake_Z, NHN_lake_z, point_imperial, point_metric
REM set lakes=BDG_DBA_nhn_hhyd_Waterbody_2
REM set streams=BDG_DBA_nhn_hnet_Network_Linear_Flow_1

call :noZ
call :withZ
call :lakes
call :streams
call :remove_empty
endlocal
goto :eof

:streams
echo. & echo --- Streams
:: fixme: BDG uses underscores in field name, NHN no separator
for %%a in (%streams%) do (
    if not exist "%%~na.gen" python %ungen% "%src%\%%a" "%%~na.gen" # # """networkFlowType""" = 1
    )
    goto :eof

:noZ
echo. & echo --- Features without Elevation values
for %%a in (%noZ%) do (
    if not exist "%%~na.gen" python %ungen% "%src%\%%a" "%%~na.gen" # #
    )
    goto :eof
    
:withZ
echo. & echo --- Elevation features
for %%a in (%Z%) do (
    if not exist "%%~na.gen" python %ungen% "%src%\%%a" "%%~na.gen" # Z_m
    )
    goto :eof

:lakes
echo. & echo --- Waterbodies and 2 line rivers
:: fixme: BDG uses underscores in field name, NHN no separator
for %%a in (%lakes%) do (
    if not exist "%%~na_lakes.gen" python %ungen% "%src%\%%a" "%%~na_lakes.gen" # # """waterDefinition""" = 4
    if not exist "%%~na_notlakes.gen" python %ungen% "%src%\%%a" "%%~na_notlakes.gen" # # """waterDefinition""" ^<^> 4
    )
    goto :eof

:remove_empty
  for %%a in (*.gen) do (
    if %%~za LSS 7 (
      echo --- Removing empty %%a
      del "%%a"
      )
    )
  goto :eof
    
:Usage
    echo.
    echo.   *** "%src%" not found
    echo.
    echo.   USAGE:  ungenerate-all [path to source gdb]
    echo.
    echo.   output .gen files are written to current directory.
    echo.
    goto :eof
    