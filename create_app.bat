@echo off
setlocal enabledelayedexpansion

rem --- Configuration ---
set "sourceFolderName=leepquest"
set "targetFileRelativePath=__init__.py"
set "stringToFind=    NAME_IN_URL = '%sourceFolderName%'"
rem --- End Configuration ---

rem --- Argument Check ---
if "%~1"=="" (
    echo WARNING: No argument provided. Please provide a name for the new folder.
    echo Usage: %~n0 NewFolderName
    goto :eof
)
if not "%~2"=="" (
    echo WARNING: Too many arguments provided. Please provide only one name for the new folder.
    echo Usage: %~n0 NewFolderName
    goto :eof
)
set "targetFolderName=%~1"
set "stringToReplace=    NAME_IN_URL = '%targetFolderName%'"


rem --- Pre-Checks ---
echo Checking prerequisites...

rem Check if source folder exists
if not exist "%sourceFolderName%\" (
    echo WARNING: Source folder '%sourceFolderName%' does not exist. Stopping.
    goto :eof
)

rem Check if __init__.py exists in source
set "sourceInitFilePath=%sourceFolderName%\%targetFileRelativePath%"
if not exist "%sourceInitFilePath%" (
    echo WARNING: File '%sourceInitFilePath%' does not exist in the source folder. Stopping.
    goto :eof
)

rem Check if the specific line exists in the source __init__.py
findstr /L /C:"%stringToFind%" "%sourceInitFilePath%" > nul 2> nul
if errorlevel 1 (
    echo WARNING: The line "%stringToFind%" was not found in '%sourceInitFilePath%'. Stopping.
    goto :eof
)

echo Prerequisites met.


rem --- Copy Folder (No longer excluding pycache) ---
echo Copying '%sourceFolderName%' to '%targetFolderName%'...
xcopy "%sourceFolderName%" "%targetFolderName%\" /E /I /Y  > nul
if errorlevel 1 (
   echo ERROR: Failed to copy the folder. Check permissions or disk space.
   goto :error_exit
)
echo Folder copied successfully.


rem --- Modify __init__.py in Target ---
set "targetInitFilePath=%targetFolderName%\%targetFileRelativePath%"
set "tempFilePath=%targetFolderName%\_init_temp.py"

if not exist "%targetInitFilePath%" (
    echo ERROR: Copied file '%targetInitFilePath%' not found. Copy operation might have failed.
    goto :error_exit
)

setlocal DisableDelayedExpansion

echo Modifying '%targetInitFilePath%'...
rem Create temp file
(
    for /f "tokens=1,* delims=:" %%A in ('findstr /N "^" "%targetInitFilePath%"') do (
        rem Assign the line content without delayed expansion
        set "current_line=%%B"
        
        rem Enable delayed expansion only for the comparison
        setlocal EnableDelayedExpansion
        REM echo DEBUG: Comparing "[!current_line!]" with "[%stringToFind%]" > con
        
        rem Compare and decide what to output
        if "!current_line!"=="%stringToFind%" (
            REM echo DEBUG: Match found! Line will be replaced. > con
            endlocal
            echo(%stringToReplace%
        ) else (
            endlocal
            rem Echo the original line WITHOUT delayed expansion
            echo(%%B
        )
    )
) > "%tempFilePath%"
if exist "%targetInitFilePath%" (
    del "%targetInitFilePath%" > nul 2> nul
)

move /Y "%tempFilePath%" "%targetInitFilePath%" > nul

rem Renaming the excel file
move /Y "%targetFolderName%\%sourceFolderName%.xlsx" "%targetFolderName%\%targetFolderName%.xlsx" > nul

echo File '%targetInitFilePath%' modified successfully.
echo ---
echo Operation completed successfully for project '%targetFolderName%'.
echo ---
goto :cleanup_and_exit

rem (The rest of the script remains the same: checking temp file, moving, etc.)

rem ... (rest of script: check temp file, move, cleanup) ...

:error_exit
echo ---
echo SCRIPT TERMINATED DUE TO ERROR.
echo ---
goto :cleanup_and_exit

:cleanup_and_exit
rem No exclusion file to clean up
endlocal
goto :eof

:eof
rem End of script