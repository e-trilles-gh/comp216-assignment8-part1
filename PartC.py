import paramiko


##PUBLIC IPv4 ADDY OF INSTANCE
HOST = '3.96.148.182'

##Using Amaonz Linux 2, default username is 'ec2-user'
USERNAME = 'ec2-user'

##KEY PATH TO THE PEM FILE THAT WAS DOWNLOADED FORM  LIGHTSAIL.
KEY_PATH = r"C:\Users\tyler\Downloads\PartC.pem"

##Declaring paths and file names
REMOTE_DIR = '/home/ec2-user/Documents'
LOCAL_FILE = 'test2.txt'
REMOTE_FILE = f'{REMOTE_DIR}/{LOCAL_FILE}'

##Creation of txt file
with open(LOCAL_FILE, 'wb') as f:
    f.write(b"This is the test file. If its not on the server the test has failed!")

    
##Parsing the PEM file into a RSAKEY and then setting up the SSH client then connecting to the server
key = paramiko.RSAKey.from_private_key_file(KEY_PATH)
ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("Should be connecting now...will find out soon")
ssh.connect(hostname=HOST, username=USERNAME, pkey=key)

##Creating the directory on the server if it doesn't exist
stdin, stdout, stderr = ssh.exec_command(f'mkdir -p {REMOTE_DIR}')
##this is just waiting for the command to finishing before moving on
stdout.channel.recv_exit_status()

print(f"{REMOTE_DIR} should be created now...")

##opening a SFTP session and uploading the file to the server
sftp = ssh.open_sftp()
sftp.put(LOCAL_FILE, REMOTE_FILE)
print(f"{LOCAL_FILE} should be uploaded to {REMOTE_DIR}")
sftp.close()

##Scanning the most rece3ntly uploaded file with clamdscan that is installed on the server.
##if it finds it to be infected it will move it to the quarantine dir otherwise it will just report it as clean. 
stdin, stdout, stderr = ssh.exec_command(f'clamdscan --infected --move=/var/quarantine {REMOTE_FILE}')
scan_output = stdout.read().decode()
print("Scan output:")
print(scan_output)

if "FOUND" in scan_output:
    print(f"{REMOTE_FILE} is infected and has been moved to /var/quarantine.")
else:
    print(f"{REMOTE_FILE} is clean.")
    
ssh.close()
print("Part C done!!")
