import sqlite3
import pandas as pd

#Had some ChatGPT help designing and building schema
def build_pollutant_measurement_tables():
    connection = sqlite3.connect('pollutant_data.db')
    cursor = connection.cursor()
    #Removing this causes an error because the data is already in the table, this isnt really an error. Our goal is to load data into SQL and the data is already loaded
    cursor.execute("DROP TABLE pollutants")
    cursor.execute("DROP TABLE place_time")
    #Note, these are all unique, which is a bit unnecessary but will prevent unique errors from occurring with the pandas filtering
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pollutants (
            id INTEGER PRIMARY KEY,
            indicator_id INTEGER,
            name TEXT NOT NULL,
            measure_method TEXT NOT NULL,   
            unit TEXT NOT NULL,
            UNIQUE (indicator_id, name, measure_method, unit)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS place_time (
            id INTEGER PRIMARY KEY,
            place TEXT NOT NULL,
            time_period TEXT NOT NULL,
            start_date TEXT NOT NULL,
            UNIQUE (place, time_period, start_date)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY,
            pollutant_id INTEGER,
            place_time_id INTEGER,
            value REAL,
            FOREIGN KEY (pollutant_id) REFERENCES pollutants(id),
            FOREIGN KEY (place_time_id) REFERENCES place_time(id)
        )
    ''')
    # cursor.execute()
    connection.commit()
    connection.close()

def print_pollutant_table():
    connection = sqlite3.connect('pollutant_data.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM pollutants''')
    # print(cursor.fetchmany(5))
    print(cursor.fetchall())
    connection.close()

def print_place_time_table():
    connection = sqlite3.connect('pollutant_data.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM place_time''')
    print(cursor.fetchmany(5))
    # print(cursor.fetchall())
    connection.close()

def print_measurements_table():
    connection = sqlite3.connect('pollutant_data.db')
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM measurements''')
    print(cursor.fetchmany(5))

    connection.close()

def get_highest_NO2_values():
    with sqlite3.connect('pollutant_data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT pollutants.name, pollutants.unit, measurements.value, place_time.place, place_time.time_period, place_time.start_date
            FROM measurements
            LEFT JOIN pollutants ON measurements.pollutant_id=pollutants.id
            LEFT JOIN place_time ON measurements.place_time_id=place_time.id
            WHERE pollutants.name = "Nitrogen dioxide (NO2)"
            ORDER BY measurements.value DESC
            LIMIT 10
        ''')
        return cursor.fetchall()

def get_recent_high_NO2_locations():
    with sqlite3.connect('pollutant_data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT pollutants.name, pollutants.unit, measurements.value, place_time.place, place_time.time_period, place_time.start_date
            FROM measurements
            LEFT JOIN pollutants ON measurements.pollutant_id=pollutants.id
            LEFT JOIN place_time ON measurements.place_time_id=place_time.id
            WHERE pollutants.name = "Nitrogen dioxide (NO2)" AND measurements.value > 40
            ORDER BY place_time.start_date DESC
            LIMIT 10
        ''')
        return cursor.fetchall()

def get_recent_high_NO2_locations_as_dataframe():
    query = '''
                SELECT pollutants.name, pollutants.unit, measurements.value, place_time.place, place_time.time_period, place_time.start_date
                FROM measurements
                LEFT JOIN pollutants ON measurements.pollutant_id=pollutants.id
                LEFT JOIN place_time ON measurements.place_time_id=place_time.id
                WHERE pollutants.name = "Nitrogen dioxide (NO2)" AND measurements.value > 40
                ORDER BY place_time.start_date DESC
                LIMIT 10
            '''
    with sqlite3.connect('pollutant_data.db') as connection:
        return pd.read_sql(query, connection)


def rename_fields(dataframe):
    dataframe = dataframe.rename(columns={
        "Indicator ID": "indicator_id",
        "Name": "name",
        "Measure": "measure_method",
        "Measure Info": "unit",
        "Geo Place Name": "place",
        "Time Period": "time_period",
        "Start_Date": "start_date"
    })
    return dataframe

def pollutant_csv_to_sql(dataframe):
    dataframe = rename_fields(dataframe)
    dataframe = dataframe[["indicator_id", "name","measure_method", "unit"]].drop_duplicates()#ChatGPT Code to clean the data before inserting, preventing Unique errors, also cleans insert syntax below
    # print(dataframe.head())
    with sqlite3.connect('pollutant_data.db') as connection:
        dataframe.to_sql("pollutants", connection, if_exists="append", index=False)
    #     dataframe.drop(['Unique ID', 'Geo Type Name',"Geo Place Name", "Time Period", "Start_Date", "Geo Join ID", "Message", "Data Value"], axis=1).to_sql("pollutants", connection, if_exists="append", index=False)

def place_time_csv_to_sql(dataframe):
    dataframe = rename_fields(dataframe)
    
    dataframe = dataframe[["place", "time_period","start_date"]].drop_duplicates()#ChatGPT Code to clean the data before inserting, preventing Unique errors, also cleans insert syntax below
    with sqlite3.connect('pollutant_data.db') as connection:
        dataframe.to_sql("place_time", connection, if_exists="append", index=False)

#Had some ChatGPT help with the planning of this function
def measurements_csv_to_sql(dataframe):
    dataframe = rename_fields(dataframe)
    connection = sqlite3.connect('pollutant_data.db')

    pollutant_df = pd.read_sql("SELECT * FROM pollutants", connection)
    place_time_df = pd.read_sql("SELECT * FROM place_time", connection)
    # place_time_df["start_date"] = pd.to_datetime(dataframe["start_date"])#ChatGPT code to fix merging error

    #add pollutant info
    dataframe = pd.merge(dataframe, pollutant_df, how="inner", left_on=["indicator_id", "name"], right_on=["indicator_id", "name"])
    dataframe = dataframe.rename(columns={"id":"pollutant_id"})

    '''Could include start_date but you need the above chatgpt code to remove an error. It would be best practice to add start_date, because it is in the UNIQUE keyword'''
    #Add the place_time info
    dataframe = pd.merge(dataframe, place_time_df, how="inner", left_on=["place", "time_period"], right_on=["place", "time_period"])
    dataframe = dataframe.rename(columns={"id":"place_time_id", "Data Value":"value"})
    dataframe = dataframe[["pollutant_id", "place_time_id", "value"]]
    dataframe.to_sql("measurements", connection, if_exists="replace", index=False)#Replacing because the entire point of this project is to get the data into SQL (this data wont change, but in the real world we would append)


    connection.close()

def csv_to_sql_tables(csv_path):
    build_pollutant_measurement_tables()
    df = pd.read_csv(csv_path, parse_dates=['Start_Date'])
    pollutant_csv_to_sql(df)
    place_time_csv_to_sql(df)
    measurements_csv_to_sql(df)
    # print_place_time_table()
    # print_pollutant_table()
    # print_measurements_table()
    

csv_to_sql_tables('venv\Air_Quality.csv')
get_highest_NO2_values()
# print(get_recent_high_NO2_locations())#Returns most recent concentrations of NO2 above 40 PPB
    
# print(get_recent_high_NO2_locations_as_dataframe().head())