import os
import stat
import requests
import shutil
from pathlib import Path
import paramiko
from paramiko import SSHClient
from scp import SCPClient
from ftplib import FTP

def download_file(url):
    """
    Downloads a file from a given URL, local file path, SCP, or FTP path.

    If the URL starts with 'http', the function attempts to download the file using the
    requests library.
    If the URL starts with 'scp', the function attempts to download the file using the
    paramiko library. This currently doesn't work well, use at your own risk.
    If the URL starts with 'ftp', the function attempts to download the file using the
    ftplib library.
    If the URL does not start with 'http', 'scp', or 'ftp', the function assumes it's a local file path
    and attempts to copy the file to a new file with the same name in the current
    directory.

    Parameters:
    url (str): The URL, SCP path, FTP path, or local file path of the file to download.

    Returns:
    None
    """
    try:
        file_path = Path(url)
        if url.startswith('http'):
            response = requests.get(url)
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            filename = file_path.name
            with open(filename, 'wb') as file:
                file.write(response.content)
        elif url.startswith('scp'):
            ssh = SSHClient()
            ssh.load_system_host_keys()
            private_key_path = "/path/to/private/key"
            mykey = paramiko.RSAKey(filename=private_key_path)
            ssh.connect('hostname', username='username', pkey=mykey)
            scp = SCPClient(ssh.get_transport())
            scp.get(url, local_path=filename)
            scp.close()
        elif url.startswith('ftp'):
            ftp = FTP('hostname')
            ftp.login(user='username', passwd='password')
            filename = file_path.name
            with open(filename, 'wb') as file:
                ftp.retrbinary('RETR ' + url, file.write)
            ftp.quit()
        else:
            if file_path.is_file():
                filename = file_path.name
                shutil.copy(url, filename)
            else:
                print("File does not exist:", url)
        # Change the permissions of the file to allow modification and deletion
        os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong with the download:", err)
    except Exception as e:
        print("An error occurred:", e, " file ", url)
