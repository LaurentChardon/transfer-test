# File Downloader
 
This project download files given their URL or path in an infinite loop, times each download, and logs the download times into a CSV file.

## Getting Started
 
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
 
### Prerequisites
 
You need Python 3 installed on your machine. You also need the following Python packages:
``` 
python-dateutil
requests
matplotlib
numpy
pandas
```

Optionally:
```  
  scp
  paramiko
  ftplib
```
You can install these packages using pip:
 
```bash
pip3 install -r requirements.txt
```
 
### Running the Script
 
To run the script, navigate to the project directory and run the following command in Linux:
 
```bash
python3 run-multi.py
```
Or, in Windows:

```
py run-multi.py
```

Replace `urls` at the bottom of the script with the URLs or local file paths you want to download.

## Generating plots

Plots can be made using the `make_plots.py` script. It requires one or more csv filenames as arguments. 
```
python3 make_plots.py *.csv

python3 make_plots.py download_times_20240223100852.csv download_times_20240223183244.csv

...
```

## Authors
 
- Laurent Chardon
 
## License
 
This project is licensed under the 2-clause BSD License - see the [LICENSE.md](LICENSE.md) file for details