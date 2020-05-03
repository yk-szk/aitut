set listfile=
call :FOREACH subroutine %listfile%
exit /b

:subroutine
jupyter nbconvert --ExecutePreprocessor.timeout=-1 --to notebook --output-dir=../docs/notebooks --execute %1
exit /b

:FOREACH
setlocal
set subroutine=%1
set listfile=%2
for /F "tokens=1" %%A in (%listfile%) do (
    call :%subroutine% %%A
)
exit /b