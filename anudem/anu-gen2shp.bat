@echo off
if "%1"=="" goto :Usage
setlocal
set o=-a_srs EPSG:3579

echo on
ogr2ogr -nlt polygon    %o% %1  NHN_HD_WATERBODY_2_lakes.gen
ogr2ogr -nlt polygon    %o% %1  NHN_HD_WATERBODY_2_notlakes.gen
ogr2ogr -nlt polygon    %o% %1  NHN_lake_z.gen
ogr2ogr -nlt point      %o% %1  point_imperial.gen
ogr2ogr -nlt point      %o% %1  point_metric.gen
ogr2ogr -nlt linestring %o% %1  contour_imperial.gen
ogr2ogr -nlt linestring %o% %1  contour_metric.gen
ogr2ogr -nlt linestring %o% %1  NHN_HN_PrimaryDirectedNLFlow_1.gen
ogr2ogr -nlt polygon    %o% %1  BDG_DBA_nhn_hhyd_Waterbody_2_lakes.gen     
ogr2ogr -nlt polygon    %o% %1  BDG_DBA_nhn_hhyd_Waterbody_2_notlakes.gen  
ogr2ogr -nlt linestring %o% %1  BDG_DBA_nhn_hnet_Network_Linear_Flow_1.gen 
ogr2ogr -nlt polygon    %o% %1  extent_105m12.gen                          
ogr2ogr -nlt polygon    %o% %1  selection_buffer_3000m.gen                 
@goto :eof


:Usage
    echo.
    echo.   Missing destination folder
    echo.
    echo.       %~0 path\to\output\shapes
    echo.
    goto :eof