@echo off
REM ---------------------------------------------------------------
REM  StakeandWager - Bounded Assistant
REM  Builds a single-file Windows executable.
REM
REM  Requires Python 3.10+ on PATH.
REM  Run this from the folder containing stakeandwager_assistant.py
REM ---------------------------------------------------------------

echo.
echo  Installing PyInstaller if needed...
python -m pip install --upgrade pyinstaller

echo.
echo  Building...
python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name "StakeandWager Assistant" ^
  --clean ^
  --noconfirm ^
  stakeandwager_assistant.py

echo.
echo  ---------------------------------------------------------------
echo   Done. The executable is in:  dist\StakeandWager Assistant.exe
echo.
echo   It needs no installation and no Python on the target machine.
echo   Records are written to:  %%USERPROFILE%%\.stakeandwager\record.jsonl
echo  ---------------------------------------------------------------
echo.
pause