for /d %%a in (dem_*) do (
    pushd %%a 
    run anu-diag2gis gis
    popd
    )