@echo --- Run ANUDEM against all .anu files in current folder
@for %%a in (*.anu) do @(
    if not exist %%~na mkdir %%~na
    if not exist %%~na\%%~na_dem.flt (
      @echo anudemc %%a
      call run start /b "%%a" cmd /c anudemc %%a
      )
    )