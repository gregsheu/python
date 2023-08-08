import paramiko
import sys
import time
ssh_client = paramiko.client.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ip = sys.argv[1]
ssh_client.connect(ip, 8822, 'admin', 'admin12345')
stdin, stdout, stderr = ssh_client.exec_command('system reboot')
stdin.close()
time.sleep(5)
print(f'STDOUT: {stdout.read().decode("utf8")}') 
