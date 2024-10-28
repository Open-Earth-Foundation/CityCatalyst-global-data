@echo off

set x=10  REM Number of times to run the command

for /l %%i in (1,1,%x%) do (
  echo Run #%%i
  python transform_script.py --input-file UAE_fuel_sales.csv --datasource-name "Ministry of Energy & Infrastructure (MEAI)" --user-input "A dataset about oil and gas sales for different regions in the United Arab Emirates (UAE) for the years 2015 to 2020 provided by the Ministry of Energy & Infrastructure (MEAI)" --show-graph
  if errorlevel 1 (
    echo Error occurred on run %%i
    exit /b 1  REM Exit if there’s an error
  )
)

echo All runs completed successfully
