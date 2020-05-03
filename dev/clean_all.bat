set listfile=
call :FOREACH subroutine %listfile%
exit /b

:subroutine
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace %1
exit /b

:FOREACH
setlocal
set subroutine=%1
set listfile=%2
for /F "tokens=1" %%A in (%listfile%) do (
    call :%subroutine% %%A
)
exit /b