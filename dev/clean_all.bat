call :FOREACH subroutine
exit /b

:subroutine
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace %1
exit /b

:FOREACH
setlocal
set subroutine=%1
for /F "tokens=1" %%A in ("*.ipynb") do (
    call :%subroutine% %%A
)
exit /b