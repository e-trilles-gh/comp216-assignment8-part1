from ftplib import FTP
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
        self.__client_file_list = []
        self.server_file_list()
        self.client_file_list()
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
        
    def server_file_list(self, directory = './ftp/upload'):
        file_list = []
        self.__ftp.cwd(directory)
        self.__ftp.dir(self.extract_filename)

    def client_file_list(self, directory = ''):
        file_list = []
        if (directory == ''):
            self.__os.getcwd()
        self.__client_file_list = self.__os.listdir()

    def upload_file(self, file_name):
        file_name = './' + file_name
        self.__ftp.cwd(self.upload_directory)
        with open(file_name, 'rb') as file:
            self.__ftp.storbinary(f'STOR {file_name}', file)

    def download_file(self, file_name):
        file_name = './' + file_name
        self.__ftp.cwd(self.upload_directory)
        with open(file_name, 'wb') as file:
            self.__ftp.retrbinary(f'RETR {file_name}', file.write)

    def delete_file(self, file_name):
        file_name = './' + file_name
        self.__ftp.cwd(self.upload_directory)
        self.__ftp.delete(file_name)

    def manage_multiple_files(self, ftp_operation):
        match ftp_operation:
            case 'upload':
                for file in self.__client_file_list:
                    self.upload_file(file)
            case 'download':
                for file in self.__server_file_list:
                    self.download_file(file)
            case 'delete':
                for file in self.__server_file_list:
                    self.delete_file(file)
                
