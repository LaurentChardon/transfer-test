import pandas as pd
import matplotlib.pyplot as plt
import argparse

def plot_times(csv_files, exclude_weekends=False):
    """
    Creates a bar graph of the mean download times obtained in the CSV files.

    The bar graph is created for the mean download times for each hour of the day.

    Create a time series plot of all the data provided
    
    Parameters:
    csv_files (list of str): The paths to the CSV files.

    Returns:
    None
    """
    # Read the headers from the first file
    headers = pd.read_csv(csv_files[0], nrows=0).columns.tolist()

    df = pd.DataFrame(columns=headers)
        
    # Loop over the list of CSV files and concatenate the data into df
    for csv_file in csv_files:
        try:
            if df.empty:
                df = pd.read_csv(csv_file)
            else:
                df = pd.concat([df, pd.read_csv(csv_file)])
        except:
            print(f"Error reading file {csv_file}")
            
    # Convert the 'Timestamp' column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y%m%d%H%M%S')
    df.set_index('Timestamp', inplace=True)
    if exclude_weekends:
        df = df[df.index.weekday < 5]

    # Extract the hour from the timestamp
    df['Hour'] = df.index.hour

    # Group the data by hour and calculate the mean and standard deviation
    count_data_points = df.groupby('Hour')[headers[1:]].count()
    mean_download_times = df.groupby('Hour')[headers[1:]].mean()
    total_data_points = count_data_points[headers[1]].sum()
    std_dev_download_times = df.groupby('Hour')[headers[1:]].std()

    # Create a bar plot with error bars
    # ax = mean_download_times.plot(kind='bar', yerr=std_dev_download_times)
    ax = mean_download_times.plot(kind='bar')
    plt.ylabel('Mean Download Time (s)')

    # Include the total number of data points in the title
    plt.title(f'Mean Download Time vs Hour of Day ({total_data_points} samples)')

    plt.show()

    # Create a time-series plot of all data
    df[headers[1:]].plot()
    plt.ylabel('Download Time (s)')
    plt.title('Time-series Plot of Download Time')

    plt.show()

if __name__ == "__main__":
    import glob

    parser = argparse.ArgumentParser(description='Plot download times from CSV files.')
    parser.add_argument('csv_files', type=str, nargs='+', help='The paths to the CSV files.')
    parser.add_argument('--exclude-weekends', action='store_true', help='Exclude weekends from the data.')

    args = parser.parse_args()

    # Expand glob patterns in the list of CSV files
    csv_files = [file for pattern in args.csv_files for file in glob.glob(pattern)]

    plot_times(csv_files, args.exclude_weekends)