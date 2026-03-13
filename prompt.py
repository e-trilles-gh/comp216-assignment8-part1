class Prompt:
    def __init__(self):
        self.__count = 0

    def capture_credentials(self):
        credentials = {'username':'', 'password':''}
        while True:
            credentials['username'] = input('Enter username: ')
            if (len(credentials['username']) > 1):
                break
        credentials['password'] = input('Enter password: ')
        return credentials
    
    def identify_operation(self):
        options = {'0':'exit', '1':'upload', '2':'download', '3':'delete'}
        while True:
            print('\n1 - Upload\n2 - Download\n3 - Delete\n0 - Exit')
            option = input('Type the number from the option: ')
            if (option in options):
                selected = options[option]
                break
        return selected
    
    def continue_operation(self, operation):
        confirm = False
        while True:
            response = input(f'Type "y" to continue {operation} or "n" to cancel: ')
            if (response.lower() == 'y'):
                confirm = True
                break
            elif (response.lower() == 'n'):
                break
        return confirm
    
    def quantify_operation(self, operation):
        options = ['0', '1', '2', '3']
        instructions = f'\n1 - {operation} individual file\n2 - {operation} all files\n3 - {operation} according to extension\n0 - exit'
        while True:
            print(instructions)
            option = input('Type the number from the option: ')
            if option in options:
                break        
        return option
        
    def finalize_exit(self):
        exit = False
        while True:
            response = input('Type "y" to confirm exit or "n" to cancel: ')
            if (response.lower() == 'y'):
                break
            elif (response.lower() == 'n'):
                exit = True
                break
        return exit
    
    def choose_file(self, operation, file_list):
        options = ['0']
        file_count = len(file_list)
        response = 'exit'
        while True:
            print(f'\nChoose the number that corresponds to the file you want to {operation}')
            for index, value in enumerate(file_list):
                count = index + 1
                options.append(str(count))
                print(f'{count} - {value}')
            print('0 - exit')
            option = input('Type the number from the option: ')
            if option in options:
                index = int(option) - 1
                if (index < 0):
                    break
                else:
                    response = file_list[index]
                    print(index)
                    type(index)
                    break
        return response
