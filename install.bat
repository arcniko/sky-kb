@echo off
REM Sky Knowledge Base — one-click installer for Windows
REM Double-click this file to install or update.

set REPO_URL=https://github.com/arcniko/sky-kb.git
set INSTALL_DIR=%USERPROFILE%\sky-kb

echo.
echo === Sky Knowledge Base Installer ===
echo.

REM Clone or pull
if exist "%INSTALL_DIR%\.git" (
    echo Updating existing install...
    git -C "%INSTALL_DIR%" pull --ff-only
    if errorlevel 1 goto :error
) else (
    if exist "%INSTALL_DIR%" (
        echo Error: %INSTALL_DIR% exists but is not a git repo.
        echo Remove it first and re-run this installer.
        echo.
        pause
        exit /b 1
    )
    echo Cloning to %INSTALL_DIR%...
    git clone "%REPO_URL%" "%INSTALL_DIR%"
    if errorlevel 1 goto :error
)

echo.

REM Sync content
echo Syncing content...
python "%INSTALL_DIR%\scripts\sync.py"
if errorlevel 1 goto :error

echo.

REM Configure Claude Desktop
echo Configuring Claude Desktop...
python "%INSTALL_DIR%\scripts\configure_claude_desktop.py" --content-dir "%INSTALL_DIR%\content"
if errorlevel 1 goto :error

echo.
echo === Done! ===
echo.
echo Restart Claude Desktop to activate the sky-knowledge tool.
echo.
pause
exit /b 0

:error
echo.
echo === Installation failed ===
echo.
pause
exit /b 1
