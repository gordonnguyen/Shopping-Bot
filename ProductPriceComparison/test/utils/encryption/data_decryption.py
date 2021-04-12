from os import access
from cryptography.fernet import Fernet
'''
key = b'pXT3l1pTRYkqoSnEUNdfNU8_-eaqGxTHoLcb0S0CoeQ='
encrypted_access = b'gAAAAABgP9lBNnD_WXuh9HRC8NGNbN9POW1F9otQXuLvVAfYvmyeLy5L2hyNCkm95mqnxhUcphhuMUiWY9DfqTk2zSmJzC_euIo3bHbn_Rto9jmUWBveTR4='
encrypted_secret = b'gAAAAABgP9lBGyBmsmDeEmWI6gizbXH1pCgsXT-ydvhbGGTADRr1yV1on-EAO1fgDI3rMmpoBYYIKd5GXcV8QdebSyPnv6vW-JMaKjexuJYhcR9NULRx23HY4PBh9mzK25L3sLqKkIdN'
'''
def readAndDecrypt(file_name):
    encrypted_file = open(file_name)
    encrypted_data = []
    encrypted_data = encrypted_file.read().split('\n')
    encrypted_file.close()
    key = encrypted_data[0]
    del encrypted_data[0]
    return decryptData(key, encrypted_data)

def decryptData(key, encrypted_data):
    f = Fernet(key)
    decrypted_data = []
    for i in range(len(encrypted_data)):
        temp_data = encrypted_data[i].encode()
        decrypted_data.append(f.decrypt(temp_data).decode())
    return decrypted_data

class aws_data:
    aws_decrypted_data = readAndDecrypt('C:/Keys/key.env')
    accessKey = aws_decrypted_data[0]
    secretKey = aws_decrypted_data[1]

'''
class bb_data:
    bb_decrypted_data = readAndDecrypt('')
'''

# Encryption method
'''
def encrypt():
    key = Fernet.generate_key()
    print('Encryption key: ', key)
    encoded_message = accessKey.encode()
    encoded_message_2 = secretKey.encode()

    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    encrypted_message_2 = f.encrypt(encoded_message_2)
    print('Encrypted access: ', encrypted_message)
    print('Encrypted secret: ', encrypted_message_2)
'''