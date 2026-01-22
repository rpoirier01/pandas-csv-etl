# Pandas CSV ETL

This is a small project I've built to familiarize myself with ETL processes and Python. For this specific project, I used air quality data found on data.gov. This project specifically filters to only 5 columns,
then removes rows that do not contain ozone data or data from a specific time frame. Additionally, functions are defined to either create CSV files after each transformation (to better follow the process) or to only
create a single, final output file.  
To expand this project, I would add command line arguments to define the type of pollutant data kept, the date range and the input/output files. 