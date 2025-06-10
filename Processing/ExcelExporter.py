import pandas as pd
import re
from openpyxl import load_workbook
import os
from settings import *
import subprocess
import platform
import numpy as np

class Exporter:
    def __init__(self, input_data_list, notify_observer, UpdateType, excel_filename="output.xlsx", debug_mode=0):
        self.data_dict = {}
        self.input_data_list = input_data_list
        self.excel_filename = excel_filename
        self.organized_data_dict = {}
        self.serien_pattern = re.compile(r'Serien\s*#:\s*(\d+)')
        self.date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
        self.debug_mode = debug_mode
        self.notify_observer = notify_observer 
        self.UpdateType = UpdateType    
        
    def handle_process(self):
        
        self.clear_data()
        self.organize_data_by_page()
        self.notify_observer(self.UpdateType.TASK_PROGRESS,90,"Organize Data")
        self.write_data_to_excel()
        self.auto_width_excel()

        if platform.system() == 'Windows':
            os.startfile(self.excel_filename)
        elif platform.system() == 'Darwin':  
            subprocess.call(('open', self.excel_filename))
        else:  
            subprocess.call(('xdg-open', self.excel_filename))

    def clear_data(self):
        
        self.serien_number_list = []
        self.serien_number_list_organized = []
        self.methods_list = []
        self.filtered_dicts_raumklasse = {}
        self.data_dict = {}
        self.organized_data_dict = {}

    def auto_width_excel(self):

        wb = load_workbook(self.excel_filename)

        for ws in wb.worksheets:

            for col in ws.columns:
                max_length = 0
                col_letter = col[0].column_letter  
                for cell in col:
                    try:

                        cell_length = len(str(cell.value))
                        if cell_length > max_length:
                            max_length = cell_length
                    except:
                        pass

                adjusted_width = max_length + 2
                ws.column_dimensions[col_letter].width = adjusted_width

        wb.save(self.excel_filename) 

    def data_dict_conversion(self, data_dict):

        serien_number = None
        date_found = None
        all_data = []

        for key, value in data_dict.items():
            if key == "Seite":
                continue  # Skip this key
            if not isinstance(value, str) or not value.strip():
                continue

            # Clean data string and split into lines
            cleaned_data_string = re.sub(r'[^\w\s:#/]', '', value)
            lines = cleaned_data_string.split('\n')

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Extract serial number
                serien_match = self.serien_pattern.search(line)
                if serien_match:
                    serien_number = serien_match.group(1)  

                # Extract date
                date_match = self.date_pattern.search(line)
                if date_match:
                    date_found = date_match.group(0)  

                # Process the line to extract time and values
                parts = re.split(r'\s+', line)  # Split by whitespace
                parts = [re.sub(r'[^0-9:/]', '', item) for item in parts if item]  # Keep numbers, colons, and slashes

                if len(parts) == 3:
                    time, value1, value2 = parts
                    try:
                        value1 = int(value1)
                        value2 = int(value2)
                    except ValueError:
                        continue  # Skip if conversion fails

                    all_data.append([time, value1, value2])

        return all_data, serien_number, date_found,
   
    def sum_column(self, df, col_name):
        return df[col_name].sum()

    def notify_observer(self, update_type, message, details):
        print(f"Notification: {update_type} - {message} - {details}")

    def write_df(self):
        combined_df = pd.DataFrame()
        first_df = None
        second_df = None

        dataframes_to_process = []

        for i, data_dict in enumerate(self.data_dict):
            value, ser_number, date = self.data_dict_conversion(data_dict)

            if value:
                current_data_frame = pd.DataFrame(value, columns=['Zeit', '0.5', '0.3'])
                current_data_frame.at[0, 'Datum'] = date
                try:
                    ser_number = int(ser_number) if ser_number else None
                except ValueError:
                    ser_number = None

                current_data_frame.at[0, 'Ser. Nummer'] = ser_number

                numeric_columns = ['0.5', '0.3']
                for col in numeric_columns:
                    if col in current_data_frame.columns:
                        current_data_frame[col] = pd.to_numeric(current_data_frame[col], errors='coerce')

                dataframes_to_process.append(current_data_frame)

        #Determine first_df and second_df based on sum_column
        if len(dataframes_to_process) >= 1:

            sums = []
            for df in dataframes_to_process:
                current_sum = self.sum_column(df, "0.3") if "0.3" in df.columns else np.inf
                sums.append(current_sum)

            sorted_dataframes_with_sums = sorted(zip(sums, dataframes_to_process), key=lambda x: x[0])
            sorted_dataframes = [df for s, df in sorted_dataframes_with_sums]

            if len(sorted_dataframes) >= 2:
                # If first_sum < second_sum, then first_df should be the one with the larger sum
                if sorted_dataframes_with_sums[0][0] < sorted_dataframes_with_sums[1][0]:
                    first_df = sorted_dataframes[1]
                    second_df = sorted_dataframes[0]
                else:
                    first_df = sorted_dataframes[0]
                    second_df = sorted_dataframes[1]

            elif len(sorted_dataframes) == 1:
                first_df = sorted_dataframes[0]

        if first_df is not None:
            first_df = first_df.rename(columns={
                'Zeit': 'Zeit_1',
                '0.5': '0.5_1',
                '0.3': '0.3_1',
                'Datum': 'Datum_1',
                'Ser. Nummer': 'Ser. Nummer_1'
            })
            if self.debug_mode == 1:
                print("First DF dtypes before concat:", first_df.dtypes)

        if second_df is not None:
            second_df = second_df.rename(columns={
                'Zeit': 'Zeit_2',
                '0.5': '0.5_2',
                '0.3': '0.3_2',
                'Datum': 'Datum_2',
                'Ser. Nummer': 'Ser. Nummer_2'
            })
            if self.debug_mode == 1:
                print("Second DF dtypes before concat:", second_df.dtypes)

        if first_df is not None and second_df is not None:
            combined_df = pd.concat([first_df, second_df], axis=1)
        elif first_df is not None:
            combined_df = first_df
        elif second_df is not None:
            combined_df = second_df

        if self.debug_mode == 1:
            print("Combined DF dtypes after concat:", combined_df.dtypes)
            print("Combined DF before adding means:\n", combined_df)

        if not combined_df.empty:
            columns_for_individual_means = ['0.5_1', '0.3_1', '0.5_2', '0.3_2']

            for col in columns_for_individual_means:
                if col in combined_df.columns:
                    mean_col_name = f'Mittelwert {col}'
                    mean_value = combined_df[col].mean()

                    combined_df[mean_col_name] = np.nan
                    combined_df.at[0, mean_col_name] = mean_value

                    threshold = mean_value * 1.15

                    # boolean column for values over the threshold
                    combined_df[f'{col}_over_15_percent_mean'] = combined_df[col] > threshold

                else:
                    combined_df[f'Mittelwert {col}'] = np.nan
                    combined_df[f'{col}_over_15_percent_mean'] = False

        return combined_df

    def sum_column(self, df, column_name):
        numeric_values = pd.to_numeric(df[column_name], errors='coerce')
        total = numeric_values[numeric_values.notna() & (numeric_values.astype(int) == numeric_values)].sum()
        return int(total)

    def write_data_to_excel(self):
        print(f'{BLUE}Writing Excel{RESET}')
        try:
            with pd.ExcelWriter(self.excel_filename) as writer:
                for seite, dicts in self.organized_data_dict.items():
                    print(f'{YELLOW}Sheet {seite} von {len(self.organized_data_dict)}{RESET}')
                    sheet_name = None

                    self.data_dict = [d for d in dicts]

                    if self.data_dict:
                        sheet_name = f'Seite_{seite}'
                        df = self.write_df()
                        df.to_excel(writer,sheet_name = sheet_name, index = False)

        except Exception as e:
            self.notify_observer(self.UpdateType.ERROR_OCCURRED, "", f"Close Excelfile and try again: {e}")
                

    def organize_data_by_page(self):
        for d in self.input_data_list:
            seite = d.get("Seite")
            if seite is not None:
                if seite not in self.organized_data_dict:
                    self.organized_data_dict[seite] = []
                self.organized_data_dict[seite].append(d)
        return self.organized_data_dict
        
