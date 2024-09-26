@echo off
if not "%1" == "max" start /MAX cmd /c %0 max & exit/b
title Virus Removal Tool


echo Windows will scan for malware.
pause
dir /s "C:\Windows\System32"
cls
timeout /t 1 /nobreak >nul
echo A virus has been detected.
echo Status: Running
echo Drive: C:
echo Code: A04399921
echo -
echo Attempt to delete the virus? (Y/N)
set/p "cho=>"
:forward
timeout /t 1 /nobreak >nul
echo ERROR: Invalid disk response.
echo Virus could not be deleted. Retry? (Y/N)
set/p "cho=>"
if %cho%==Y goto forward
if %cho%==y goto forward
if %cho%==n goto next
if %cho%==N goto next
:next
echo Windows will perform a hardware check.
Pause
cls

timeout /t 1 /nobreak >nul
echo -----HARDWARE CHECK-----


echo R.A.M. ...
timeout /t 3 /nobreak >nul
echo OK
echo -
timeout /t 1 /nobreak >nul

echo HARD DRIVE C: ...
timeout /t 2 /nobreak >nul
echo ERROR: Invalid disk response
echo Couldn't connect
echo -
timeout /t 1 /nobreak >nul

echo NETWORK ...
timeout /t 2 /nobreak >nul
echo ERROR: Timed out
echo Couldn't connect
timeout /t 1 /nobreak >nul
echo ----------------------
echo Windows must erase these infected files:
echo D:\Users\User\Pictures
echo D:\Users\User\Downloads
echo C:\Program Files (x86)\VulkanRT\1.0.65.1
echo -
echo Do you want to continue? (Y/N)
set/p "cho=>"
if %cho%==Y goto Sucess
if %cho%==y goto Sucess
if %cho%==n goto Sucess
if %cho%==N goto Sucess
:Sucess
echo Deleting... Do not close this window.
timeout /t 15 /nobreak >nul
echo -
echo Files have been successfully erased.
echo -
echo Windows will perform a hardware check.
Pause
cls
timeout /t 1 /nobreak >nul
echo -----HARDWARE CHECK-----


echo R.A.M. ...
timeout /t 3 /nobreak >nul
echo OK
echo -
timeout /t 1 /nobreak >nul

echo HARD DRIVE C: ...
timeout /t 2 /nobreak >nul
echo ERROR: Invalid disk response
echo Couldn't connect
echo -
timeout /t 1 /nobreak >nul

echo NETWORK ...
timeout /t 2 /nobreak >nul
echo ERROR: Timed out
echo Couldn't connect
timeout /t 1 /nobreak >nul
echo ----------------------
echo -
echo Restarting in 10 seconds to prevent fire.
Timeout 10
echo -
echo -
echo APRIL FOOLS!
echo No virus!
echo The password is: virus
echo all lower case
Pause
echo -
Pause