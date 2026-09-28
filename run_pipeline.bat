@echo off

cd /d "D:\VS CODE\Automated Sales Analytics Pipeline"

call .venv\Scripts\activate

python pipeline\pipeline.py

echo.
echo Pipeline execution completed.

pause