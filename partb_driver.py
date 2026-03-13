from ftp_connection import FTPConnection
from ftplib import FTP, error_perm, error_reply
from prompt import Prompt
from dotenv import load_dotenv
import os, threading

class PartBDriver:
    load_dotenv()
    
    def __init__(self, host = os.getenv('FTP_HOST'), user_name = os.getenv('FTP_USER'), password = os.getenv('FTP_PASSWORD')):
        self.host = host
        self.username = user_name
        self.password = password
        self.prompter = None
        self.client = None
        
    @property
    def user_name(self):
        return self.username
    
    def extract_extension(self, file_list):
        extensions = list({f.split('.')[-1] for f in file_list})
        return extensions
    
    def sort_files(self, file_list, extension):
        extension = '.' + extension
        sorted_files = [f for f in file_list if f.endswith(extension)]
        return sorted_files
    
    def upload_file(self, operation):
        # get the present working directory
        directory = self.client.client_current_directory
        
        # get the list of all files and directory at a given path
        client_file_list = self.client.client_file_list(directory)
        
        # capture the desired client operation
        response = self.prompter.quantify_operation(operation)
        
        if (response == '1'):
            # capture the file for upload
            file_response = self.prompter.choose_file(operation, client_file_list)
            
            # upload the selected file
            if (file_response != 'exit'):
                
                self.client.upload_file(file_response)
                
        elif (response == '2'):
            # upload all files except directories
            self.client.manage_multiple_files(operation)
            
        elif (response =='3'):
            # identify extensions
            extensions = self.extract_extension(client_file_list)
            
            # user is asked to pick the extension for upload
            extension = self.prompter.choose_file(operation, extensions)
            
            if (extension != 'exit'):
                # files with identified extesion are saved in list
                sorted_files = self.sort_files(client_file_list, extension)
                
                # save the identified files for upload 
                self.client.file_list = sorted_files
                
                # perform the upload of all files with same extension
                self.client.manage_multiple_files(operation)
            return
        else:
            return
        
    def download_file(self, operation):
        # capture the desired action from user - single or multiple download
        response = self.prompter.quantify_operation(operation)
        
        #directory = '/home/' + self.user_name + '/ftp/upload'
        
        # retrieve the file list from server directory
        server_file_list = self.client.server_file_list()
        
        # download single file
        if (response == '1'):
            # ask the user of which file to download
            selected_file = self.prompter.choose_file(operation, server_file_list)
            
            # download the selected file
            self.client.download_file(selected_file)
        
        # download all the files from the server
        elif (response == '2'):
            self.client.manage_multiple_files(operation)
            
        elif (response == '3'):
            
            # extract all the extensions from the files
            extensions = self.extract_extension(server_file_list)
        
            # user is asked to pick the extension for upload
            extension = self.prompter.choose_file(operation, extensions)
            
            if (extension != 'exit'):
                # files with identified extesion are saved in list
                sorted_files = self.sort_files(server_file_list, extension)
                
                # store the sorted file list for download
                self.client.server_list = sorted_files
                
                # perform the upload of all files with same extension
                self.client.manage_multiple_files(operation)
            return
        else:
            return
        
    def delete_file(self, operation):
        #directory = '/home/' + self.user_name + '/ftp/upload'
        #print(directory)
        
        # capture the desired action from user - single or multiple delete
        response = self.prompter.quantify_operation(operation)
        
        # retrieve the file list from server directory
        server_file_list = self.client.server_file_list()
        
        # delete single file
        if (response == '1'):
            # ask the user of which file to delete
            selected_file = self.prompter.choose_file(operation, server_file_list)
            
            # delete the selected file
            self.client.delete_file(selected_file)
        
        # delete all the files from the server
        elif (response == '2'):
            self.client.manage_multiple_files(operation)
            
        elif (response == '3'):
            # extract all the extensions from the files
            extensions = self.extract_extension(server_file_list)
        
            # user is asked to pick the extension for upload
            extension = self.prompter.choose_file(operation, extensions)
            
            if (extension != 'exit'):
                # files with identified extesion are saved in list
                sorted_files = self.sort_files(server_file_list, extension)
                
                # store the sorted file list for delete
                self.client.server_list = sorted_files
                
                # perform the delete of all files with same extension
                self.client.manage_multiple_files(operation)
            return
        else:
            return        

    def run_driver(self, bool_flag):
        self.prompter = Prompt()
        isConnected = bool_flag
        print(bool_flag)
        process = ''
        
        self.client = FTPConnection(self.host,self.username, self.password)
        print(f'host: {self.host}, username: {self.username}, pass: {self.password}')
        
        isTransferring = True
        while (isConnected == True):
            exit = False

            while True:
                #self.client.server_current_directory() = '/home/' + self.username + '/ftp/upload'
                process = self.prompter.identify_operation()
                match process:
                    case 'upload':
                        self.upload_file(process)
                    case 'download':
                        self.download_file(process)
                    case 'delete':
                        self.delete_file(process)
                    case 'exit':
                        print('\nDo you want to exit transferring data?')
                        isTransferring = self.prompter.finalize_exit()
                if (isTransferring == False):
                    break
                
            print('\nDo you wnat to exit FTP connection?')
            exit = self.prompter.finalize_exit()
            isConnected = exit
        
        self.client.quit_connection()
        print('Exiting program')
        