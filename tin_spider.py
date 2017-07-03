#! /usr/bin/env python3


import re
import subprocess


def getKey():
    with open('tin_spider_log', 'wb') as f:
        subprocess.run(['wget', 'github.com/manjaro/packages-core/raw/master/manjaro-keyring/manjaro.gpg'], stdout=f, stderr=f)

        subprocess.run(['sudo', 'gpg', '--import', 'manjaro.gpg'], stdout=f, stderr=f)


def verifySig(sig):
    try:
        with open('tin_spider_log', 'r+') as f:
            subprocess.run(['sudo', 'gpg', '--verify', sig], stdout=f, stderr=f)
        with open('tin_spider_log', 'r') as f:
            for line in f.readlines():
                #print(line)
                if re.findall('^gpg: Good*', line) or re.findall('^Primary*', line):
                    print(line, end='')
    except Exception as e:
        print('There was an error! Check the log.')
    

def verifyCheckSum(iso, checksum):
    value = subprocess.run(['sudo', 'sha1sum', iso], stdout=subprocess.PIPE)
    decoded_value = value.stdout.decode('utf-8')
    with open(checksum, 'r') as f:
        if f.readline() == decoded_value:
            print('ISO is Good to Go!')
        else:
            print("Something didn't line up.")


if __name__ == '__main__':
    getKey()
    subprocess.run(['ls'])
    print('What is the name of the signature file? (.sig)')
    signature = input('>> ')
    print('What is the name of the iso file? (.iso)')
    iso = input('>> ')
    print('What is the name of the checksum file? (.sha*)')
    checksum = input('>> ')
    verifySig(signature)
    verifyCheckSum(iso, checksum)

    
