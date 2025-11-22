# Script para ejecutar todas las pruebas
# Windows: run_tests.bat

@echo off
echo ====================================
echo Ejecutando Suite de Pruebas
echo ====================================
echo.

echo [1/4] Ejecutando pruebas unitarias...
pytest tests/unit/ -v
if %errorlevel% neq 0 (
    echo ERROR: Pruebas unitarias fallaron
    exit /b 1
)
echo.

echo [2/4] Ejecutando pruebas de integracion...
pytest tests/integration/ -v
if %errorlevel% neq 0 (
    echo ERROR: Pruebas de integracion fallaron
    exit /b 1
)
echo.

echo [3/4] Ejecutando prueba E2E...
pytest tests/e2e/ -v
if %errorlevel% neq 0 (
    echo ERROR: Prueba E2E fallo
    exit /b 1
)
echo.

echo [4/4] Ejecutando analisis estatico...
bandit -r src/ -c .bandit
if %errorlevel% neq 0 (
    echo ERROR: Analisis estatico fallo
    exit /b 1
)
echo.

echo ====================================
echo TODAS LAS PRUEBAS PASARON - OK
echo ====================================
