## SEEG

It is quicker to process the data locally and add the raw data output to s3 bucket. Running through mage on our instance is slow, but should be fine when doing transformation by sector. To get the raw data output follow these steps.

1. Download data folder Dados por município 11.1 (make sure to download the top folder and not a subdirectory): https://drive.google.com/drive/folders/1rdVratpALksJJlRG-H3jMOCAmRMq4gXq

3. Run the script CityCatalyst-global-data/cc-mage/local_scripts/seeg_file_to_rawdata.sql on a local instance of Duckdb. Make sure to change directories based on your file structure.

4. Upload the folder seeg_city_emissions to s3.