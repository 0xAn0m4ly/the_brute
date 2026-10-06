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

# Ftp
def ftp():
    while True:
        for number, mode in ftp_modes.items():
            print(number + ' -> ' + mode)
        selected_mode = input(
            'Please select the ftp option from the previos ones by typing the correspondive number.\t'
            )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit
        elif selected_mode == 1:
            ftp_mode_1()
        elif selected_mode == 2:
            ftp_mode_2()
        elif selected_mode == 3:
            ftp_mode_3()
        else:
            print('Mode not found, please try again.')


def input_mode():
    while True:
        print('Welcome...')
        for letter, mode in modes.items():
            print(letter + ' -> ' + mode)
        selected_mode = input(
            'Choose the protocol by typing the correspondive letter or type "q" to quit the program.\t'
        )
        if selected_mode == 'q':
            print('Bye!')
            sys.exit()
        elif selected_mode == 'a':
            ftp()
        else:
            print('Mode not found, please try again.')