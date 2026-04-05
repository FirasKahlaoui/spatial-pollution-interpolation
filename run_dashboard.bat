@echo off
echo Starting WaterWatch: China Heavy Metals Dashboard...
echo Open your browser and navigate to http://localhost:8000
echo.
python -m http.server 8000 --directory webapp
pause
