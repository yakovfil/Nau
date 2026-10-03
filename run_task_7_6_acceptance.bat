@echo off
setlocal EnableExtensions DisableDelayedExpansion

rem Run the six native visual checks required by OpenSpec task 7.6.
rem Each application stays open until the reviewer closes its window.
set "ROOT=%~dp0"
set "ENGINE=%ROOT%NauEngineLite"
set "DEMO=%ROOT%NauDemo"
set "ENGINE_BIN=%ENGINE%\build\replace-eastl-msvc-static\bin"
set "REPORT=%ENGINE%\build\task-7.6-human-acceptance.txt"

if /I "%~1"=="--help" goto usage
if not "%~1"=="" if /I not "%~1"=="--list" goto usage_error

call :require "%ENGINE_BIN%\Debug\SceneBaseSample.exe"
if errorlevel 1 exit /b 1
call :require "%ENGINE_BIN%\Debug\inputDemo.exe"
if errorlevel 1 exit /b 1
call :require "%DEMO%\bin\Debug\NauDemo.exe"
if errorlevel 1 exit /b 1
call :require "%ENGINE_BIN%\Release\SceneBaseSample.exe"
if errorlevel 1 exit /b 1
call :require "%ENGINE_BIN%\Release\inputDemo.exe"
if errorlevel 1 exit /b 1
call :require "%DEMO%\bin\Release\NauDemo.exe"
if errorlevel 1 exit /b 1

echo Task 7.6 binaries, in run order:
call :show Debug SceneBaseSample "%ENGINE_BIN%\Debug\SceneBaseSample.exe" "%ENGINE%"
call :show Debug inputDemo "%ENGINE_BIN%\Debug\inputDemo.exe" "%ENGINE%"
call :show Debug NauDemo "%DEMO%\bin\Debug\NauDemo.exe" "%DEMO%\bin\Debug"
call :show Release SceneBaseSample "%ENGINE_BIN%\Release\SceneBaseSample.exe" "%ENGINE%"
call :show Release inputDemo "%ENGINE_BIN%\Release\inputDemo.exe" "%ENGINE%"
call :show Release NauDemo "%DEMO%\bin\Release\NauDemo.exe" "%DEMO%\bin\Release"

if /I "%~1"=="--list" exit /b 0

set "FAILURES=0"
set "SKIPPED=0"
> "%REPORT%" echo Task 7.6 human acceptance - %DATE% %TIME%
>> "%REPORT%" echo Configuration^|Target^|Executable^|ExitCode^|ReviewerResult

call :run Debug SceneBaseSample "%ENGINE_BIN%\Debug\SceneBaseSample.exe" "%ENGINE%"
call :run Debug inputDemo "%ENGINE_BIN%\Debug\inputDemo.exe" "%ENGINE%"
call :run Debug NauDemo "%DEMO%\bin\Debug\NauDemo.exe" "%DEMO%\bin\Debug"
call :run Release SceneBaseSample "%ENGINE_BIN%\Release\SceneBaseSample.exe" "%ENGINE%"
call :run Release inputDemo "%ENGINE_BIN%\Release\inputDemo.exe" "%ENGINE%"
call :run Release NauDemo "%DEMO%\bin\Release\NauDemo.exe" "%DEMO%\bin\Release"

echo.
echo Results: "%REPORT%"
type "%REPORT%"
if not "%FAILURES%"=="0" (
    echo One or more checks failed.
    exit /b 1
)
if not "%SKIPPED%"=="0" (
    echo Some checks were skipped; acceptance is incomplete.
    exit /b 2
)
echo All six checks passed.
exit /b 0

:require
if exist "%~1" exit /b 0
echo Missing required binary: "%~1"
echo Build the Debug and Release engine samples and NauDemo before running task 7.6.
exit /b 1

:show
echo   %~1 %~2: "%~3"
echo     Working directory: "%~4"
exit /b 0

:run
set "CONFIGURATION=%~1"
set "TARGET=%~2"
set "EXECUTABLE=%~3"
set "WORKING_DIRECTORY=%~4"
echo.
echo Running %CONFIGURATION% %TARGET%. Inspect the scene and input, then close its primary window.
if /I "%TARGET%"=="inputDemo" echo Check both windows and input. The secondary window alone does not quit the app.
start "" /wait /d "%WORKING_DIRECTORY%" "%EXECUTABLE%"
set "EXIT_CODE=%ERRORLEVEL%"
echo Process exit code: %EXIT_CODE%
choice /c YNS /n /m "Were scene/input behavior and normal close correct? [Y]es [N]o [S]kip: "
set "REVIEW_CHOICE=%ERRORLEVEL%"
set "RESULT=SKIPPED"
if "%REVIEW_CHOICE%"=="1" set "RESULT=PASS"
if "%REVIEW_CHOICE%"=="2" set "RESULT=FAIL"
if "%REVIEW_CHOICE%"=="3" set "RESULT=SKIPPED"
if not "%EXIT_CODE%"=="0" set "RESULT=FAIL"
if "%RESULT%"=="FAIL" set /a FAILURES+=1 >nul
if "%RESULT%"=="SKIPPED" set /a SKIPPED+=1 >nul
>> "%REPORT%" <nul set /p "=%CONFIGURATION%|%TARGET%|%EXECUTABLE%|%EXIT_CODE%|%RESULT%"
>> "%REPORT%" echo(
echo Recorded: %RESULT%
exit /b 0

:usage
echo Usage: %~nx0 [--list]
echo Run without arguments for the six interactive checks.
exit /b 0

:usage_error
echo Unknown argument: %~1
echo Usage: %~nx0 [--list]
exit /b 2
