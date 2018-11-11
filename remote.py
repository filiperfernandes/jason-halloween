from pexpect import pxssh
import getpass

def connect(hostname, username, password, key):

    COMMAND = 'echo "' + key + '" > key.txt'

    try:
        s = pxssh.pxssh()
#        hostname = raw_input('hostname: ')
#        username = raw_input('username: ')
#        password = getpass.getpass('password: ')
        s.login (hostname, username, password)
        s.sendline (COMMAND)   # run a command
        s.prompt()             # match the prompt
#        print (s.before)          # print everything before the prompt.
        #Leave connection oppen on purpose
        #s.logout()
    except pxssh.ExceptionPxssh as e :
        print ("pxssh failed on login.")
        print (str(e))
