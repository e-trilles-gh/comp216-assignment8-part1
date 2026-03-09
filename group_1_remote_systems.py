from ftplib import FTP, error_reply, error_proto
import threading

#Part A:

ftp_server = 'ftp.gnu.org'
directory = 'video'
file_extension = 'webm'
webm_list = list()
file_url_list = list()
threads = list()

def access_ftp_server():
    ftp = FTP(ftp_server)
    ftp.login()
    ftp.cwd(directory)
    
    return ftp

def retrieve_webm_url_list():
    webm_list = []
    file_list = []
    try:
        ftp = access_ftp_server()
        ftp.retrlines('LIST', callback = file_list.append)

        print('List of all files')

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


webm_list = retrieve_webm_url_list()

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

#PartB