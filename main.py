# ChatGPT suggested project and data, with occasional AI help

import pandas as pd
from datetime import datetime


data_frame = pd.read_csv('Air_Quality.csv', parse_dates=['Start_Date'])


def filter_to_date_place_value(csv_data_frame, output_path):
    csv_data_frame.drop(['Unique ID', 'Indicator ID', 'Measure Info', 'Geo Type Name', 'Geo Join ID', 'Message'], axis=1).to_csv(output_path, index=False) #dont use index as a column

def filter_to_date_place_value_in_place(csv_data_frame):
    csv_data_frame.drop(['Unique ID', 'Indicator ID', 'Measure Info', 'Geo Type Name', 'Geo Join ID', 'Message'], axis=1, inplace=True)
    return csv_data_frame
    
def filter_only_ozone(csv_data_frame, output_path):
    csv_data_frame[csv_data_frame['Name']=='Ozone (O3)'].to_csv(output_path, index=False) #dont use index as a column

def filter_only_ozone_in_place(csv_data_frame):
    print('After filtering to only Ozone data ' + str(csv_data_frame[csv_data_frame['Name']=='Ozone (O3)'].shape[0]) + ' rows remain')
    return csv_data_frame[csv_data_frame['Name']=='Ozone (O3)']

def filter_to_2025(csv_data_frame, output_path, start_date, end_date): #Had ChatGPT help with Syntax
    #csv_data_frame[str(csv_data_frame['Start_Date']).str.contains("2025")].to_csv('./Air_Quality_2025.csv', index=False)

    #csv_data_frame[csv_data_frame['Start_Date'] <= jan_2026 and csv_data_frame['Start_Date'] >= jan_2025 ].to_csv('./Air_Quality_2025.csv', index=False)
    csv_data_frame[(csv_data_frame['Start_Date'] >= start_date) & (csv_data_frame['Start_Date'] <= end_date )].to_csv(output_path, index=False)
    print('After filtering to the specific time range ' + str(pd.read_csv(output_path).shape[0]) + ' records remain')


## Added logging at each step, which gives an indication of how many rows were removed after each operation (no logging after columns were removed because this does not impact the row count)
def ozone_data_cleaned_2025(original_csv_data_frame, output_csv_path, save_middle_steps):
    start_date = datetime(2021, 1, 1, 0, 0, 0)
    end_date = datetime(2025, 1, 1, 0, 0, 0)
    # print(filter_only_ozone_in_place(filter_to_date_place_value_in_place(original_csv_data_frame)))
    if save_middle_steps:
        print('The original CSV contained ' + str(original_csv_data_frame.shape[0]) + ' rows')
        filter_to_date_place_value(original_csv_data_frame, 'Trimmed_Air_Quality.csv')
        trimmed_csv_data_frame = pd.read_csv('Trimmed_Air_Quality.csv')
        filter_only_ozone(trimmed_csv_data_frame, 'Ozone_Data_Trimmed.csv')
        trimmed_ozone_csv_data_frame = pd.read_csv('Ozone_Data_Trimmed.csv', parse_dates=['Start_Date'])
        print('After filtering to only Ozone ' + str(trimmed_ozone_csv_data_frame.shape[0]) + ' records remain')
        filter_to_2025(trimmed_ozone_csv_data_frame, output_csv_path, start_date, end_date)
        #final_csv_data_frame = pd.read_csv(output_csv_path)
        #print('After filtering to the specific time range ' + str(pd.read_csv(output_csv_path).shape[0]) + ' records remain')
    else:
        print('The original CSV contained ' + str(original_csv_data_frame.shape[0]) + ' rows')
        filter_to_2025(filter_only_ozone_in_place(filter_to_date_place_value_in_place(original_csv_data_frame)), output_csv_path, start_date, end_date)
    

ozone_data_cleaned_2025(data_frame, 'Air_Quality_Test_Long.csv', True)