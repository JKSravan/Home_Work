import pandas as pd
import numpy as np
import os
import random

# Function to fetch 10 consecutive data points from a CSV file starting from a random index
def fetch_consecutive_data_points(csv_file):
    # Read CSV
    df = pd.read_csv(csv_file)
    num_points = len(df)
    
    if num_points < 10:
        return None
    
    # Select a random starting index (ensure at least 10 points are left)
    start_index = random.randint(0, num_points - 10)
    
    # Select 10 consecutive data points
    selected_data = df.iloc[start_index:start_index+10]
    return selected_data

# Function to predict next 3 values based on selected data points
def predict_next_three_values(data_points):
    n_values = data_points['stock price'].values
    
    # Sort to find the 2nd highest value
    sorted_values = np.sort(n_values)
    second_highest = sorted_values[-2]
    
    # Predict n+1, n+2, n+3
    n1 = second_highest
    n2 = n1 - (n_values[-1] - n1) / 2
    n3 = n2 - (n1 - n2) / 4
    
    return n1, n2, n3

# Function to process files for a given exchange
def process_exchange_files(exchange_folder, num_files_to_sample):
    files = os.listdir(exchange_folder)
    num_files_processed = 0
    
    for file in files:
        if num_files_processed >= num_files_to_sample:
            break
        
        csv_file = os.path.join(exchange_folder, file)
        output_file = os.path.splitext(file)[0] + '_output.csv'
        print(output_file)
        # Fetch consecutive data points
        selected_data = fetch_consecutive_data_points(csv_file)
        
        if selected_data is None:
            continue
        
        # Predict next 3 values
        n1, n2, n3 = predict_next_three_values(selected_data)
        
        # Append predictions to output file
        with open(output_file, 'w') as f:
            # Write original data
            f.write(selected_data.to_csv(index=False))
            
            # Write predictions
            f.write(f"{selected_data.iloc[-1]['Stock-ID']}, Timestamp-n+1, {n1}\n")
            f.write(f"{selected_data.iloc[-1]['Stock-ID']}, Timestamp-n+2, {n2}\n")
            f.write(f"{selected_data.iloc[-1]['Stock-ID']}, Timestamp-n+3, {n3}\n")
        
        num_files_processed += 1

# Main function to orchestrate the process
def main():
    # Assume exchange_folders is a list of folders containing CSV files for each exchange
    exchange_folders = ['exchange1_folder','exchange2_folder']
    num_files_to_sample = 2
    
    for exchange_folder in exchange_folders:
        if os.path.isdir(exchange_folder):
            process_exchange_files(exchange_folder, num_files_to_sample)
            

if __name__ == "__main__":
    main()
