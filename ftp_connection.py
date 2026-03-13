from ftplib import FTP, error_perm
import os

class FTPConnection:
    def __init__(self, host, username, password):
        self.__ftp = FTP()
        self.__os = os
        self.__ftp.connect(host=host, port=21)
        self.__ftp.login(user=username, passwd=password)
        self.__upload_directory = '/ftp/upload'
        self.__selected_file = ''
        self.__server_file_list = []
        self.__client_file_list = self.client_file_list()
        self.__server_current_directory = self.__ftp.pwd()
        self.__client_current_directory = self.__os.getcwd()
    
    @property
    def upload_directory(self):
        return self.__upload_directory

    @property    
    def selected_file(self):
        return self.__selected_file

    @property    
    def server_current_directory(self):
        return self.__server_current_directory

    @property
    def client_current_directory(self):
        return self.__client_current_directory

    @property
    def file_list(self):
        return self.__client_file_list
    
    @property
    def server_list(self):
        return self.__server_file_list
    
    @server_list.setter
    def server_list(self, file_list):
        self.__server_file_list = file_list
    
    @file_list.setter
    def file_list(self, file_list):
        self.__client_file_list = file_list    
    
    @client_current_directory.setter
    def client_current_directory(self, directory_name):
        if (directory_name == '1'):
            self.__os.chdir('..')
        else:
            path = f'{self.client_current_directory}\{directory_name}'
            self.__os.chdir(path)
        self.__client_current_directory = self.__os.getcwd()

    @server_current_directory.setter
    def server_current_directory(self, directory_name):
        if (directory_name == '1'):
            self.__ftp.cwd('..')
        else:
            path = f'{self.server_current_directory}/{directory_name}'
            self.__ftp.cwd(path)
        self.__server_current_directory = self.__ftp.pwd()
    
    def extract_filename(self, line):
        filename = line.split()[-1]
        self.__server_file_list.append(filename)
    
    def thread_process(self, process):
        threads = []
        
        for file in self.__client_file_list:
            try:
                th = threading.Thread(target=process, args=(file,))
                threads.append(th)
                th.start()
                #self.upload_file(file)
            except error_perm:
                print(f'{file} is a directory, not a file.')
            except Exception:
                print(f'Error while uploading {file}.')        
        
        
        for thread in threads:
            thread.join()
        return
    
    def server_file_list(self, directory = '/ftp/upload'):
        file_list = []
        self.__ftp.cwd(directory)
        self.__ftp.dir(self.extract_filename)
        return self.__server_file_list

    def client_file_list(self, directory = ''):
        if (directory == ''):
            self.__os.getcwd()
        return self.__os.listdir()

    def upload_file(self, file_name):
        file_name = './' + file_name
        self.__ftp.cwd(self.upload_directory)
        with open(file_name, 'rb') as file:
            self.__ftp.storbinary(f'STOR {file_name}', file)
            print(f'{file_name} uploaded')

    def download_file(self, file_name):
        file_name = './' + file_name
        self.__ftp.cwd(self.upload_directory)
        with open(file_name, 'wb') as file:
            self.__ftp.retrbinary(f'RETR {file_name}', file.write)
            print(f'{file_name} downloaded')

    def delete_file(self, file_name):
        file_name = './' + file_name
        self.__ftp.cwd(self.upload_directory)
        self.__ftp.delete(file_name)
        print(f'{file_name} deleted')

    def manage_multiple_files(self, ftp_operation):
        match ftp_operation:
            case 'upload':
                self.thread_process(self.upload_file)
                #for file in self.__client_file_list:
                    #try:
                        #self.upload_file(file)
                    #except error_perm:
                        #print(f'{file} is a directory, not a file.')
                    #except Exception:
                        #print(f'Error while uploading {file}.')
            case 'download':
                for file in self.__server_file_list:
                    try:
                        self.download_file(file)
                    except error_perm:
                        print(f'{file} is a directory, not a file.')
                    except Exception:
                        print(f'Error while downloading {file}.')                    
            case 'delete':
                for file in self.__server_file_list:
                    try:
                        self.delete_file(file)
                    except error_perm:
                        print(f'{file} is a directory, not a file.')
                    except Exception:
                        print(f'Error while deleting {file}.')
                        
    def quit_connection(self):
        self.__ftp.quit()
