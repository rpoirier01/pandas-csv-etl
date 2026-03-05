# Pandas CSV ETL
## Project Explanation
This is a small project I've built to familiarize myself with ETL processes and Python. For this specific project, I used air quality data found on data.gov. This project is divided into two parts:  
- Filtering and visualizing only Ozone data
- Loading data into SQLite, establishing a relational database and writing queries  
The ozone section filters to only 5 columns, then removes rows that do not contain ozone data or data from a specific time frame. Additionally, functions are defined to either create CSV files after each transformation (to better follow the process and allow traceability) or to only create a single, final output file. Visualizations are creating using Jupyter in visualize.ipynb, including seeing the 10 
locations with the highest Ozone pollution, seeing Ozone changes over time in West Queens and seeing Ozone changes over time in a pivot table.  

The SQL section loads the CSV, and writes into three separate tables: pollutants, place_time and measurements. The pollutants table stores information related to each type of pollutant, including its name,
measurement unit and type of measurement. The place_time table stores information related to when and where the measurement was collected, including the place, the start date of the measurement and the period
in which the measurement was taken. Finally the measurements table includes references to the ids of the pollutants and place_time tables, along with the measurement itself.  

## Project Expansion
To expand this project, I would add command line arguments to define the type of pollutant data kept, the date range and the input/output files. I would also add in visualization for the SQL part of this project.

### Note on AI Usage
I had some help troubleshooting logic and syntax from AI, this project was initially suggested by AI. Some code in load_sql.py is AI generated or based off of AI generated code.  
