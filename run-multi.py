import csv
import os
import timeit
from download import download_file
from make_plots import plot_times
from datetime import datetime
import time

filename = f"download_times_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

def download_files_in_loop(urls):
    """
    Downloads a file from two different URLs in an infinite loop and logs the download times to a CSV file.

    Parameters:
    urls (str): The URLs of the files to download.

    Returns:
    None
    """
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Time Taken for http", "Time Taken for T.O. shared file", "Time Taken for shared file"])
        try:
            while True:
                now = datetime.now().strftime('%Y%m%d%H%M%S')
                times_taken = []

                for url in urls:
                    start_time = timeit.default_timer()
                    download_file(url)
                    end_time = timeit.default_timer()
                    time_taken = end_time - start_time
                    times_taken.append(time_taken)
                    if os.path.exists("10MB"):
                        os.remove("10MB")
                    else:
                        print("The file does not exist")

                writer.writerow([now] + times_taken)
                file.flush()  # Flush the file to disk

                print(f"{now} - " + " - ".join(f"{url}: {time_taken:.3f} seconds" for url, time_taken in zip(['http','T.O shared','Shared'], times_taken)))
                time.sleep(600. - sum(times_taken))  # Sleep for 10 minutes (600 seconds)

        except KeyboardInterrupt:
            # Not handling this for now
            pass

# URLs to download files from
urls= ['http://nodrahc.com/10MB', '//ECONM3HWVFSP007.ncr.int.ec.gc.ca/SscThroughputTestSpace/10MB', '//int.ec.gc.ca/shares/T/TRANSFERT/CharlesD/10MB']
download_files_in_loop(urls)
plot_times(filename)