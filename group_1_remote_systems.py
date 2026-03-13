from ftplib import FTP, error_reply, error_proto
import threading

#Part A:

ftp_server = 'ftp.gnu.org'
directory = 'video'
file_extension = 'webm'
webm_list = list()
file_url_list = list()
threads = list()

# access the ftp server
def access_ftp_server():
    ftp = FTP(ftp_server)
    ftp.login()
    ftp.cwd(directory)

    return ftp

# get all the list url for processing
def retrieve_webm_url_list():
    webm_list = []
    file_list = []
    try:
        # access the server and create a list of all the files
        ftp = access_ftp_server()
        ftp.retrlines('LIST', callback = file_list.append)

        print('List of all files')

        # iterate through the list
        for file in file_list:
            print(file)

        for item in file_list:
            item_split = item.split('.')
            if item_split[-1] == file_extension:
                item_split = item.split(' ')
                webm_list.append(item_split[-1])
        ftp.quit()
    except error_reply as rep:
        print('unexpected server reply error.' , rep)
    except error_perm as pro:
        print('server permission error.', pro)
    except Exception as e:
        print(f'Error: {e}')
        
    return webm_list

def download_file(file_name):
    try:
        ftp = access_ftp_server()
        with open(file_name, 'wb') as webm_file:
            ftp.retrbinary(f'RETR {file_name}', webm_file.write, blocksize=50)
        ftp.quit()
    except error_reply as rep:
        print('unexpected server reply error.' , rep)
    except error_perm as pro:
        print('server permission error.', pro)
    except Exception as e:
        print(f'Error: {e}')

def thread_download():
    print('List of all webm files')
    for webm in webm_list:
        print(webm)

        #extracts name for the running thread
        thread_name = webm

        #creates thread for the method
        #with url argument
        th = threading.Thread(
            target = download_file,
            name = thread_name,
            args = (webm,)
        )

        #appends each created thread to the list
        threads.append(th)

        #starts the thread after being created
        th.start()

    for thread in threads:

        #ensures that all threads are finished before
        #proceeding to the rest of the code
        thread.join()

webm_list = retrieve_webm_url_list()
thread_download()




#PartB

from ftp_connection import FTPConnection
from partb_driver import PartBDriver
from prompt import Prompt
from dotenv import load_dotenv
import os

load_dotenv()
prompter = Prompt()

# test code from .env
host = os.getenv('FTP_HOST')
#username = os.getenv('FTP_USER')
#password = os.getenv('FTP_PASSWORD')

# dictionary for username and password
credentials = {}

# this for loop check for the valid credential from the user for 3x
for i in range(3):
    try:
        # test code from .env
        # client = FTPConnection(host, username, password)
        # client.quit_connection()    
        
        # functioning code
        credentials = prompter.capture_credentials()
        client = FTPConnection(host,credentials['username'], credentials['password'])
        client.quit_connection()
        break
    except error_reply:
        print(f'Check your username or password are correct.')
    except Exception:
        print('Error while logging in')

#driver = PartBDriver(user_name=username, password=password)

# functioning code
driver = PartBDriver(user_name=credentials['username'], password=credentials['password'])

# run the whole ftp client from other class
driver.run_driver(True)

print('end')
