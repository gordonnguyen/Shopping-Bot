from cryptography.fernet import Fernet
'''
key = b'pXT3l1pTRYkqoSnEUNdfNU8_-eaqGxTHoLcb0S0CoeQ='
encrypted_access = b'gAAAAABgP9lBNnD_WXuh9HRC8NGNbN9POW1F9otQXuLvVAfYvmyeLy5L2hyNCkm95mqnxhUcphhuMUiWY9DfqTk2zSmJzC_euIo3bHbn_Rto9jmUWBveTR4='
encrypted_secret = b'gAAAAABgP9lBGyBmsmDeEmWI6gizbXH1pCgsXT-ydvhbGGTADRr1yV1on-EAO1fgDI3rMmpoBYYIKd5GXcV8QdebSyPnv6vW-JMaKjexuJYhcR9NULRx23HY4PBh9mzK25L3sLqKkIdN'
'''
encrypted_file = open('key.env')


encrypted_access = encrypted_file.readline().strip().encode()
encrypted_secret = encrypted_file.readline().strip().encode()
print(key)

f = Fernet(key)
accessKey = f.decrypt(encrypted_access).decode()
secretKey = f.decrypt(encrypted_secret).decode()

encrypted_file.close()



def decrypt():
    key = encrypted_file.readline().strip().encode()
    encrypted = encrypted_file.readline().strip().encode()
    f = Fernet(key)
    encrypted = 

# Encryption method
'''
def main():
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